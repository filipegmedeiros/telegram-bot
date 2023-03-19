import locale
import re
from datetime import datetime

from telebot.formatting import escape_markdown

from service.purchase_service import PurchaseService

COMMANDS = {
    'start': 'Gives information about the bot',
    'help': 'Gives information about all of the available commands',
    'ping': 'Measure the execution time to run test and send a message'
}


def is_command(text):
    pattern = re.compile(r'^([+-])(\d+(,\d{2})?)(\s+\S+( \S+)*)+(\s+(\d+/\d+|\d+(\.\d+)?))?$')
    return bool(pattern.fullmatch(text))


class BotService:

    def __init__(self, purchase_service: PurchaseService):
        self.purchase_service = purchase_service

    def add_purchase(self, chat_id: int, purchase_string: str):
        return self.purchase_service.save_purchase(chat_id, purchase_string)

    def list_debts(self, chat_id: int):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        # get current month and year
        now = datetime.now()
        current_month = now.strftime("%m")
        current_year = now.strftime("%y")

        # get all purchases due for this month
        due_purchases = self.purchase_service.get_purchases_due_month(chat_id)

        # calculate total due and create the markdown string
        total_due = sum(p.value_month if p.operator == '+' else -p.value_month for p in due_purchases)

        total = f"R$ {total_due:.2f}"

        month_name = now.strftime("%B").upper()

        header = f"```> DÍVIDAS PARA 10/{current_month}/{current_year} - PAGAR EM {month_name} <"
        lines = [
            f"{p.operator}{p.value_month:.2f}".ljust(12) +
            f"({p.installments[0]}/{p.installments[1]})".ljust(7) +
            f"  ->  {escape_markdown(p.product_name)}"
            for p in due_purchases
        ]
        lines_end = "-" * len(header)
        footer = f"Total do Mês: ``` *{total}* "
        message = "\n".join([header, "-" * len(header)] + lines + [lines_end] + [footer])
        return self.escape_markdown(message)

    @staticmethod
    def escape_markdown(text: str) -> str:
        return text.replace("-", "\\-").replace(">", "\\>") \
            .replace("+", "\\+").replace(".", ",").replace("(", "\\(").replace(")", "\\)")