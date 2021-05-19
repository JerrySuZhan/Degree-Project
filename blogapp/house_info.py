import pandas as pd


class HouseInfo(object):
    def __init__(self, fpath):
        self.df = pd.read_csv(fpath)

    def query_by_ids(self, ids):
        target_df = pd.DataFrame(list(ids), columns=["id"])
        df_target = pd.merge(left=target_df, right=self.df)

        return df_target

    def get_title_by_id(self, house_id):
        return self.df[self.df["id"] == int(house_id)]["address"].iloc[0]

    def get_genres_by_id(self, house_id):
        return self.df[self.df["id"] == int(house_id)]["district"].iloc[0]

    def get_total_price_by_id(self, house_id):
        return self.df[self.df["id"] == int(house_id)]["total_price"].iloc[0]

    def get_price_per_meter_by_id(self, house_id):
        return self.df[self.df["id"] == int(house_id)]["price_per_meter"].iloc[0]

    def get_size_by_id(self, house_id):
        return self.df[self.df["id"] == int(house_id)]["size"].iloc[0]