from main.bot import send_message
from main.parser import parser_factory
from main.service import get_employees_info


def main():
    """
    Project entry point.
    """
    parser = parser_factory()
    args = parser.parse_args()

    data = get_employees_info(next_day=args.next_day)
    send_message(employee_data=data, next_day=args.next_day)


if __name__ == "__main__":
    main()
