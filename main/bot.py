from jinja2 import Environment, FileSystemLoader
from telegram import ParseMode
from telegram.bot import Bot

from main import config

env = Environment(
    loader=FileSystemLoader(config.TEMPLATES_PATH), trim_blocks=True, lstrip_blocks=True
)
template = env.get_template(config.TEMPLATE_FILE)


def send_message(employee_data: dict, next_day: bool):
    """
    Send formatted message to specific chat id.
    """
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)

    is_absent = any(
        [*employee_data.get("vacation", []), *employee_data.get("illness", [])]
    )

    chat_ids = config.TELEGRAM_CHAT_ID.split(",")

    for chat_id in chat_ids:
        bot.send_message(
            chat_id=chat_id,
            text=template.render(
                is_absent=is_absent,
                next_day=next_day,
                vacation=employee_data.get("vacation"),
                illness=employee_data.get("illness"),
                birthday=employee_data.get("birthday"),
                anniversary=employee_data.get("anniversary"),
            ),
            parse_mode=ParseMode.HTML,
        )
