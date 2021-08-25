import re
from collections import defaultdict
from functools import partial
from typing import Dict, List

import dateparser
import requests

from main import config, const
from main.const import AbsentReason, EventType
from main.exceptions import CSRF_TOKEN_NOT_FOUND, CsrfTokenNotFoundException
from main.logs import create_logger
from main.utils import get_current_date

logger = create_logger(__name__)


class HurmaService:
    """
    Hurma API service for extraction users activity info.
    """

    CSRF_TOKEN_RE = r'name="_token" value="(.+)\">'

    def __init__(self, next_day: bool = False):
        self.cookies = self._make_auth_request()
        self.get_current_date = partial(get_current_date, next_day=next_day)

    def get_users_timeline(self) -> List[dict]:
        """
        Make pagination requests and extract all timeline info about each user.

        :return: List with user timelines for current month.
        """
        timeline_data = []

        total_pages = self._get_total_timeline_pages()

        for page in range(1, total_pages + 1):
            params = {
                "month": self.get_current_date(date_format=const.DEFAULT_MONTH_FORMAT),
                "page": page,
            }
            page_response = self._make_api_request(
                endpoint=const.USERS_TIMELINE_ENDPOINT, params=params
            )
            timeline_data.extend(page_response["employees"])

        return timeline_data

    def get_absent_user_ids(self, timelines: List[dict]) -> List[int]:
        """
        Extract user ids for users which absent for current day.
        """
        absent_user_ids = []

        for user_data in timelines:
            for day in user_data["schedule_days"]:
                if len(day["activity_data"]) and self._compare_dates(date=day["date"]):
                    absent_user_ids.append(user_data["id"])

        logger.info(f"Get {len(absent_user_ids)} absent user.")

        return absent_user_ids

    def get_absent_users_info(self, users_id: List[int]) -> dict:
        """
        Get all info about absent user.
        """
        users_info = defaultdict(list)

        for user_id in users_id:
            base_user_info = self._get_base_absent_user_info(user_id=user_id)
            user_name = self._get_user_name(user_id=user_id)
            user_contact = self._get_user_contact(user_id=user_id)
            user_contact = user_contact[0] if user_contact else None

            for reason in [AbsentReason.vacation_ru, AbsentReason.illness_ru]:
                if base_user_info["reason"] == reason:
                    users_info[const.ABSENT_REASON_MAP[reason]].append(
                        {
                            **base_user_info,
                            "user_name": user_name,
                            "user_contact": user_contact,
                        }
                    )

        return dict(users_info)

    def get_users_events(self) -> Dict[str, list]:
        """
        Return all events for current date.
        """
        params = {"date": self.get_current_date()}

        response = self._make_api_request(
            endpoint=const.USER_EVENTS_ENDPOINT, params=params
        )

        events_info = defaultdict(list)

        for event in response["events"]:
            if event["eventName"].startswith(EventType.anniversary_ru):
                events_info[EventType.anniversary].append(
                    {
                        "user_name": event["name"],
                        "date": self.get_current_date(),
                        "years": self._extract_anniversary(
                            event_name=event["eventName"]
                        ),
                    }
                )

            if event["eventName"].startswith(EventType.birthday_ru):
                events_info[EventType.birthday].append(
                    {
                        "user_name": event["name"],
                        "day": self.get_current_date(
                            date_format=const.EVENT_DATE_FORMAT
                        ),
                    }
                )

        return dict(events_info)

    def _get_base_absent_user_info(self, user_id: int) -> dict:
        """
        Extract base data about user activity for specific user.
        """
        params = {
            "employee_id": user_id,
            "date": self.get_current_date(),
        }

        response = self._make_api_request(
            endpoint=const.USER_SCHEDULE_DATA_ENDPOINT, params=params
        )
        user_info = {
            "user_id": response["people_id"],
            "reason": response["activity_data"][0]["name"],
            "period": response["activity_data"][0]["date_period"],
            "days_left": self._calculate_days_left(
                date=response["activity_data"][0]["date_period"]["to"]
            ),
        }
        return user_info

    def _get_user_name(self, user_id: int) -> str:
        """
        Extract full name of specific user.
        """
        params = {"employee_id": user_id}

        response = self._make_api_request(
            endpoint=const.USER_NAME_ENDPOINT, params=params
        )
        return response["data"]["name"]

    def _get_user_contact(self, user_id: int) -> List[str]:
        """
        Extract Telegram account of specific user.
        """
        params = {"employee_id": user_id}

        response = self._make_api_request(
            endpoint=const.USER_CONTACTS_ENDPOINT, params=params
        )
        return [
            item["value"].replace("@", "")
            for item in response
            if item["type"] == const.TELEGRAM_CONTACT_ID
        ]

    def _get_total_timeline_pages(self) -> int:
        """
        Extract total pages in pagination.
        This value depend on amount of employees registered in Hurma service.

        :return: Int number with total pages.
        """
        params = {
            "month": self.get_current_date(date_format=const.DEFAULT_MONTH_FORMAT),
            "page": 1,
        }
        response = self._make_api_request(
            endpoint=const.USERS_TIMELINE_ENDPOINT, params=params
        )
        return response["meta"]["last_page"]

    def _make_auth_request(self) -> Dict[str, str]:
        """
        Make Request to Hurma Login endpoint.
        Extract CSRF token and make request again for extract
        login session cookies.

        :return: Response cookies after success login.
        """
        login_url = config.HURMA_HOST + const.LOGIN_ENDPOINT

        logger.info(f"Make request to: {login_url} to obtain CSRF token.")

        login_page_response = requests.get(url=login_url)
        logger.info(f"Response status: {login_page_response.status_code}")

        token = re.search(pattern=self.CSRF_TOKEN_RE, string=login_page_response.text)

        if not token:
            raise CsrfTokenNotFoundException(CSRF_TOKEN_NOT_FOUND)

        token = token.group(1)
        logger.info(f"Got CSRF token: {token}")

        form_data = {
            "_token": token,
            "email": config.HURMA_EMAIL,
            "password": config.HURMA_PASSWORD,
        }

        logger.info(f"Make request to: {login_url} to login user.")

        login_response = requests.post(
            url=login_url, data=form_data, cookies=login_page_response.cookies
        )
        logger.info(f"Response status: {login_response.status_code}")

        return dict(login_response.cookies)

    def _make_api_request(self, endpoint: str, params: dict) -> dict:
        """
        Make Request to Hurma API endpoint with specific query params.

        :param endpoint: Api endpoint that will concat with base host.
        :param params: Dict with params that will be added to endpoint.
        :return: Response from API in JSON format.
        """
        api_url = config.HURMA_HOST + endpoint.format(**params)

        logger.info(f"Make request to endpoint: {api_url} .")

        api_resp = requests.get(
            url=api_url, headers=const.DEFAULT_HEADERS, cookies=self.cookies
        )
        logger.info(f"Response status: {api_resp.status_code}")

        return api_resp.json()

    def _compare_dates(
        self, date: str, date_format: str = const.DEFAULT_DATE_FORMAT
    ) -> bool:
        """
        Check if `date` is today date.
        """
        return date.split(" ")[0] == self.get_current_date(date_format=date_format)

    def _calculate_days_left(self, date: str) -> int:
        """
        Calculate amount of days between `date` and current date.
        """
        date_to = dateparser.parse(date)
        current_date = dateparser.parse(self.get_current_date())
        return (date_to - current_date).days + 1

    @staticmethod
    def _extract_anniversary(event_name: str) -> int:
        """
        Return user anniversary.
        """
        return int(event_name.split(" ")[-2])


def get_employees_info(next_day: bool = False) -> dict:
    """
    Return all data about employee.
    """
    service = HurmaService(next_day=next_day)

    timelines = service.get_users_timeline()
    absent_users_ids = service.get_absent_user_ids(timelines=timelines)
    absent_user_info = service.get_absent_users_info(users_id=absent_users_ids)

    user_events = service.get_users_events()

    return {**absent_user_info, **user_events}
