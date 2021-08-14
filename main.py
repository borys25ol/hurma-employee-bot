from main.bot import send_message
from main.service import get_employees_info


def main():
    """
    Project entry point.
    """
    data = get_employees_info()
    send_message(employee_data=data)


if __name__ == "__main__":
    main()
