#!/usr/bin/env python
# coding: utf-8

# ##  生成Embedding的几种方法
import os

import findspark

# findspark.init("E:\spark_home")
findspark.init()
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
import pandas as pd
import numpy as np
from pyspark.ml.feature import Word2Vec
from pyspark.sql import functions as F
from pyspark.sql import types as T
import csv

sc = SparkContext('local')
spark = SparkSession(sc)

class Embedding2(object):
    def __int__(self):
        print("init!!!!")

    def pre(self):
        filename1 = os.path.dirname(os.path.dirname(__file__)) + r'\blogapp\resources\buildings.csv'

        # file = open(filename1)
        # reader = csv.reader(file)
        #
        # original = list(reader)
        # content = csv.writer(file)
        #
        # content.writerow(["3", "cherry", "Eng"])
        # file.close()

        # 1. 内容向量word2vec
        df = pd.read_csv(filename1)

        # 用cut分组
        total_price_groups = pd.cut(df['total_price'], bins=[0, 200, 400, 600, 800, 1000000],
                                    labels=['低价格', '稍低价格', '中价格', '中高价格', '高价格'])
        print(df.groupby(total_price_groups)[['id']].count())
        df['total_price'] = total_price_groups

        # 用cut分组
        price_per_meter_groups = pd.cut(df['price_per_meter'], bins=[0, 20000, 40000, 60000, 80000, 1000000],
                                        labels=['低价格', '稍低价格', '中价格', '中高价格', '高价格'])
        print(df.groupby(price_per_meter_groups)[['id']].count())
        df['price_per_meter'] = price_per_meter_groups

        # 用cut分组
        size_groups = pd.cut(df['size'], bins=[0, 60, 90, 120, 150, 10000], labels=['低价格', '稍低价格', '中价格', '中高价格', '高价格'])
        print(df.groupby(size_groups)[['id']].count())
        df['size'] = size_groups

        df['total_price'] = df['total_price'].astype('object')
        df['price_per_meter'] = df['price_per_meter'].astype('object')
        df['size'] = df['size'].astype('object')

        filename2 = os.path.dirname(os.path.dirname(__file__)) + r'\blogapp\resources\buildings2.csv'
        df.to_csv(filename2, index=False)

        df["newColumn"] = df["district"] + " " + df['total_price'] + " " + df['price_per_meter'] + " " + df[
            'num_of_bedrooms'].map(str) + " " + df['num_of_living_rooms'].map(str) + " " + df['size'] + " " + df[
                              'building_type']


        filename3 = os.path.dirname(os.path.dirname(__file__)) + r'\blogapp\resources\test.csv'
        df.to_csv(filename3, index=False)

        filename4 = os.path.dirname(os.path.dirname(__file__)) + r'\blogapp\resources\test.csv'
        documentDF = spark.read.option("header", True).csv(filename4)

        # 把非常的字符串格式变成LIST形式
        documentDF = documentDF.withColumn('newColumns', F.split(documentDF.newColumn, " "))

        # Learn a mapping from words to Vectors.
        word2Vec = Word2Vec(vectorSize=5, minCount=0, inputCol="newColumns", outputCol="vector")
        model = word2Vec.fit(documentDF)

        vector = model.transform(documentDF)

        filename5 = os.path.dirname(os.path.dirname(__file__)) + r'\blogapp\resources\test2.csv'
        model.transform(documentDF).select("id", "vector").toPandas().to_csv(filename5, index=False)

        # df_embedding = pd.read_csv("./datas/test2.csv")

        # df_movie = pd.read_csv("./datas/buildings2.csv")
        #
        # df_merge = pd.merge(left=df_embedding,
        #                     right=df_movie,
        #                     left_on="id",
        #                     right_on="id")
        #
        # import numpy as np
        # import json
        #
        # df_merge["result"] = df_merge["result"].map(lambda x: np.array(json.loads(x)))
        #
        # # 随便挑选一个电影：4018	What Women Want (2000)
        # id = 2
        # df_merge.loc[df_merge["id"] == id]
        #
        # movie_embedding = df_merge.loc[df_merge["id"] == id, "result"].iloc[0]
        #
        # # 余弦相似度
        # from scipy.spatial import distance
        #
        # df_merge["sim_value"] = df_merge["result"].map(lambda x: 1 - distance.cosine(movie_embedding, x))
        # df_merge[["id", "district", "address", "price_per_meter", "sim_value"]].head(3)
        # df_merge.sort_values(by="sim_value", ascending=False)[
        #     ["id", "district", "address", "price_per_meter", "total_price", "num_of_bedrooms", "num_of_living_rooms", "size",
        #      "building_type", "sim_value"]].head(20)
