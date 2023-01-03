from pymongo import MongoClient
import pandas as pd


class FoodData:
    def __init__(self,CONNECTION_URL):
        self.cluster = MongoClient(CONNECTION_URL)
        self.database = self.cluster["FoodData"]
        self.collection = self.database["dataset"]
    def retrieve_all_data(self,):
        return pd.DataFrame(list(self.collection.find())).drop('_id',axis=1).to_dict("records")
    def test(self,):
        return pd.read_csv("dataset.csv",compression='gzip')