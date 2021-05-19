#!/usr/bin/env python
# coding: utf-8


# ### 1. 获取数据
import os

import pandas as pd
import findspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.ml.feature import Word2Vec
import numpy as np
import json
from scipy.spatial import distance


class Embedding(object):
    def __int__(self):
        print("init!!!!")

    def pre(self):

        filename1 = os.path.dirname(os.path.dirname(__file__)) + r'/blogapp/resources/ratings.csv'
        df = pd.read_csv(filename1)

        # 只取平均分以上的数据，作为喜欢的列表
        df = df[df["ratings"] > df["ratings"].mean()].copy()

        # 聚合得到userId，movieId列表
        df_group = df.groupby(['user_id'])['house_id'].apply(lambda x: ' '.join([str(m) for m in x])).reset_index()

        filename2 = os.path.dirname(os.path.dirname(__file__)) + r'/blogapp/resources/movielens_uid_movieids.csv'
        df_group.to_csv(filename2, index=False)

        # ### 3. 使用Pyspark训练item2vec

        findspark.find()
        findspark.init()

        spark = SparkSession.builder.appName("PySpark Item2vec").getOrCreate()

        sc = spark.sparkContext

        # #### Pyspark读取CSV数据
        filename3 = os.path.dirname(os.path.dirname(__file__)) + r'/blogapp/resources/movielens_uid_movieids.csv'
        df = spark.read.csv(filename3, header=True)

        # 把非常的字符串格式变成LIST形式
        df = df.withColumn('house_ids', F.split(df.house_id, " "))

        # #### 实现word2vec的训练与转换
        # https://spark.apache.org/docs/2.4.6/ml-features.html#word2vec
        word2Vec = Word2Vec(
            vectorSize=5,
            minCount=0,
            inputCol="house_ids",
            outputCol="house_2vec")
        model = word2Vec.fit(df)

        # # 不计算每个user的embedding，而是计算item的embedding
        # model.getVectors().show(3, truncate=False)
        #
        # model.getVectors().select("word", "vector").toPandas().to_csv('./resources/movielens_movie_embedding.csv', index=False)

        # #### 实现word2vec的训练与转换
        result = model.transform(df)
        result[['user_id', 'house_2vec']].show(3, truncate=False)

        filename4 = os.path.dirname(os.path.dirname(__file__)) + r'/blogapp/resources/movielens_user_embedding.csv'
        model.transform(df).select("user_id", "house_2vec").toPandas().to_csv(filename4,
                                                                             index=False)

        # # ### 4. 对于给定电影算出最相似的10个电影
        # df_embedding = pd.read_csv("./resources/movielens_movie_embedding.csv")
        # df_movie = pd.read_csv("./resources/movies.csv")
        # df_merge = pd.merge(left=df_embedding,
        #                     right=df_movie,
        #                     left_on="word",
        #                     right_on="movieId")
        #
        # df_merge["vector"] = df_merge["vector"].map(lambda x: np.array(json.loads(x)))
        #
        # # 随便挑选一个电影：4018	What Women Want (2000)
        # movie_id = 4018
        # df_merge.loc[df_merge["movieId"] == movie_id]
        #
        # movie_embedding = df_merge.loc[df_merge["movieId"] == movie_id, "vector"].iloc[0]
        #
        # # 余弦相似度
        #
        # df_merge["sim_value"] = df_merge["vector"].map(lambda x: 1 - distance.cosine(movie_embedding, x))
        #
        # df_merge[["movieId", "title", "genres", "sim_value"]].head(3)
        #
        # # 按相似度降序排列，查询前10条
        # print(df_merge.sort_values(by="sim_value", ascending=False)[["movieId", "title", "genres", "sim_value"]].head(10))
