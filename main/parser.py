from argparse import ArgumentParser


def parser_factory() -> ArgumentParser:
    """
    Create arg parser configured for project.
    """
    parser = ArgumentParser()

    parser.add_argument(
        "--next_day",
        required=False,
        action="store_true",
        help="Check employees info for next day",
        default=False,
    )

    return parser
