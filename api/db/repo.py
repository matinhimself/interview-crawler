from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo import UpdateOne
from .pconf import MONGOURI, DATABASE


class Repository:
    def __init__(self):
        self.client = MongoClient(MONGOURI)
        self.db = self.client[DATABASE]
        self.companies_collection = self.db['companies_esg']

    def get_company_by_ric(self, ric):
        return self.companies_collection.find_one(
            filter={
                "_id": ric
            }
        )

    def get_companies_names_like(self, name, limit=10, skip=0):
        return self.companies_collection.find(
            filter={
                "name": {
                    "$regex": f"^{name}"
                }
            },
            projection={

                "name": 1,
            },
            limit=limit,
            skip=skip
        )

    def insert_companies(self, companies):
        try:
            changed = self.companies_collection.insert_many(
                companies,
                ordered=False
            )
        except BulkWriteError:
            pass

    def upsert_companies(self, companies):
        upserts = [
            UpdateOne(
                {'_id': x['_id']},
                {'$setOnInsert': x},
                upsert=True) for x in companies
        ]
        return self.companies_collection.bulk_write(
            upserts
        ).upserted_count
