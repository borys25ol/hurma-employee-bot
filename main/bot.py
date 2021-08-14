from jinja2 import Environment, FileSystemLoader
from telegram import ParseMode
from telegram.bot import Bot

from main import config

env = Environment(
    loader=FileSystemLoader(config.TEMPLATES_PATH), trim_blocks=True, lstrip_blocks=True
)
template = env.get_template(config.TEMPLATE_FILE)


def send_message(employee_data: dict):
    """
    Send formatted message to specific chat id.
    """
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)

    has_absent = any([*employee_data["vacation"], *employee_data["illness"]])

    return bot.send_message(
        chat_id=config.TELEGRAM_CHAT_ID,
        text=template.render(
            is_absent=has_absent,
            vacation=employee_data["vacation"],
            illness=employee_data["illness"],
            birthday=employee_data["birthday"],
            anniversary=employee_data["anniversary"],
        ),
        parse_mode=ParseMode.HTML,
    )
