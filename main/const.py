class EventType:
    """
    Class for storing event types.
    """

    anniversary = "anniversary"
    birthday = "birthday"


class AbsentReason:
    """
    Class for storing absent reason.
    """

    vacation = "vacation"
    illness = "illness"


# Logging message format.
LOG_FORMAT = "[%(asctime)s] %(message)s"

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_MONTH_FORMAT = "%m-%Y"

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