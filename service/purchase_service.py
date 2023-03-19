from datetime import datetime
from typing import List

from model.purchase_model import Purchase
from repository.purchase_repository import PurchaseRepository


class PurchaseService:

    def __init__(self, purchase_repository: PurchaseRepository):
        self.purchase_repository = purchase_repository

    @staticmethod
    def message_to_purchase(user_uuid: int, message: str) -> Purchase:
        parts = message.split(' ')
        product_name = ''
        operator = parts[0][0]
        total_price = float(parts[0][1:].replace(',', '.'))
        ratio = 1.0
        installments = (1, 1)
        for part in parts[1:]:

            if '/' in part:
                installments = tuple(map(int, part.split('/')))
            elif '.' in part:
                ratio = float(part)
            else:
                product_name = product_name + part + ' '
        value_month = (total_price / int(installments[1])) * ratio
        return Purchase(user_uuid=user_uuid, operator=operator, product_name=product_name.strip(),
                        value_month=value_month, total_price=total_price, installments=installments,
                        ratio=ratio, bought_at=datetime.now(),
                        )

    def save_purchase(self, chat_id, purchase_string):
        purchase: Purchase = self.message_to_purchase(chat_id, purchase_string)
        self.purchase_repository.create(purchase)

    def get_purchases_due_month(self, user_uuid: int) -> List[Purchase]:
        due_purchases = self.purchase_repository.get_all_by_user_uuid_and_month(user_uuid)

        due_purchases = [p for p in due_purchases if p.installments[0] <= p.installments[1]]

        # sort by installments, value_month and bought_at
        due_purchases.sort(key=lambda p: (p.installments[1] - p.installments[0], -p.value_month, p.bought_at),
                           reverse=True)
        return due_purchases
