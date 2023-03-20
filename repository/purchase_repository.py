import os
from typing import List, Optional

from bson import ObjectId
from pymongo import MongoClient

from model.purchase_model import Purchase


class PurchaseRepository:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.collection = self.client['compras-bot']['purchases']

    def create(self, purchase: Purchase):
        self.collection.insert_one(purchase.dict(by_alias=True))

    def update_due_purchases(self, user_uuid: str):
        query = {
            'user_uuid': user_uuid,
        }
        due_purchases = self.collection.find(query)

        for purchase in due_purchases:
            if purchase["installments"][0] == purchase["installments"][1]:
                # If it's the last installment, remove the purchase document
                self.collection.delete_one({"_id": purchase["_id"]})
            else:
                # Otherwise, increment the installment
                new_installments = (purchase["installments"][0] + 1, purchase["installments"][1])
                self.collection.update_one({"_id": purchase["_id"]}, {"$set": {"installments": new_installments}})

    def get_all_by_user_uuid_and_month(self, user_uuid: int) -> List[Purchase]:

        query = {
            'user_uuid': str(user_uuid),
        }

        purchases = [Purchase(**p) for p in self.collection.find(query)]

        purchases.sort(key=lambda p: (p.installments[1] - p.installments[0], p.value_month, p.bought_at),
                       reverse=True)

        return purchases

    def delete(self, purchase_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(purchase_id)})
        return result.deleted_count > 0

    def update(self, purchase_id: str, purchase: Purchase) -> Optional[Purchase]:
        purchase_dict = purchase.dict(by_alias=True)
        result = self.collection.update_one(
            {"_id": ObjectId(purchase_id)}, {"$set": purchase_dict}
        )
        if result.modified_count > 0:
            purchase.id = purchase_id
            return purchase
        else:
            return None

    def get_all_users_uuid(self) -> List[str]:
        uuids = self.collection.distinct("user_uuid")
        return uuids
