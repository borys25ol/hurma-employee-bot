class EventType:
    """
    Class for storing event types.
    """

    anniversary = "anniversary"
    anniversary_ru = "Годовщина"
    birthday = "birthday"
    birthday_ru = "День рождения"


class AbsentReason:
    """
    Class for storing absent reason.
    """

    vacation = "vacation"
    vacation_ru = "Отпуск"
    illness = "illness"
    illness_ru = "Больничный"


ABSENT_REASON_MAP = {
    AbsentReason.vacation_ru: AbsentReason.vacation,
    AbsentReason.illness_ru: AbsentReason.illness,
}

# Logging message format.
LOG_FORMAT = "[%(asctime)s] %(message)s"

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_MONTH_FORMAT = "%m-%Y"
EVENT_DATE_FORMAT = "%d %B"

DEFAULT_HEADERS = {"x-requested-with": "XMLHttpRequest"}

# Hurma API endpoints.
LOGIN_ENDPOINT = "/login"
USERS_TIMELINE_ENDPOINT = (
    "/timeline/vue/get-timeline-data?month={month}&page={page}"
    "&order=%7B%22field%22:%22name%22,%22direction%22:%22asc%22%7D"
    "&teams=[]&search=&requests=[]&approved=[]"
)

USER_SCHEDULE_DATA_ENDPOINT = (
    "/timeline/vue/get-schedule-day-data?employee_id={employee_id}&date={date}"
)
USER_NAME_ENDPOINT = "/employee/vue/common/info?employee_id={employee_id}"
USER_CONTACTS_ENDPOINT = "/employee/vue/contacts?employee_id={employee_id}"
USER_EVENTS_ENDPOINT = "/calendar/api/day?day={date}"

# Each type of contact has specific ID.
# We need only telegram account.
TELEGRAM_CONTACT_ID = 5
