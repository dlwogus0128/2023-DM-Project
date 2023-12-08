from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
import os
import json
import pyspark
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from collections import Counter
from pyspark.ml.fpm import FPGrowth
from itertools import combinations
import json
import re
from matplotlib import font_manager as fm, pyplot as plt, rc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np
import konlpy as k
import pandas as pd
import networkx as nx
import matplotlib as mat
from sklearn.metrics.pairwise import cosine_similarity
from pyspark.sql import functions as F

# Setting Env Variables
os.environ["PYSPARK_PYTHON"]="D:\Anaconda\envs\k-ium\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"]="D:\Anaconda\envs\k-ium\Lib\site-packages\pyspark"
os.environ["JAVA_HOME"]="C:\Program Files\Java\jdk-1.8"
os.environ["PYTHON_HOME"]="D:\Anaconda\envs\k-ium\python.exe"
os.environ["HADOOP_HOME"]="D:\Hadoop"

# Opening Patent Data File
patent_file_path = "D:\\GIT\\2023-DM-Project\\patent.json"
with open(patent_file_path, "r", encoding="utf-8") as file:
    patent_data = json.load(file)
    
    
# ##### 1. PreProcessing Data #####

# Extracting patent_name, ipc, application date, applicants from the original data
all_patents = [patent["patent_name"] for data in patent_data for patent in data["patents"]]
all_patents_ipc = [patent["ipc"] for data in patent_data for patent in data["patents"]]
all_patents_dates = [patent["application_date"] for data in patent_data for patent in data["patents"]]
all_patents_applicants = [patent["applicant"] for data in patent_data for patent in data["patents"]]

# Define IPC Start, End Index (Start index included, End index not included)

ipc_start_index=1
ipc_end_index=5

# Extracting Main, Sub IPC Code and make string to use in final query
def extract_patents_main_sub_ipc(ipc_list:list, start_idx:int, end_idx:int) -> list:
    ipc_main_sub_list=[]
    for ipcs in ipc_list:
        ipc_list = []
        for ipc_item in ipcs:
            if len(ipc_list)!=0:
                if ipc_list[0]!=ipc_item[start_idx:end_idx]:
                    ipc_list.append(ipc_item[start_idx:end_idx])
                    break
            else:
                ipc_list.append(ipc_item[start_idx:end_idx])
        ipc_main_sub_list.append(ipc_list)
    return ipc_main_sub_list

patents_main_sub_ipc=extract_patents_main_sub_ipc(all_patents_ipc,ipc_start_index,ipc_end_index)
all_patents_ipc_string = [" ".join(ipc) for ipc in patents_main_sub_ipc]

# Extract Korean and remove duplicated spaces
def preprocess_text(text):
    results = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text)
    results = re.sub(r"\s+", " ", results).strip()
    return results

preprocessed_patent_names = [preprocess_text(name) for name in all_patents]
# detokenized_patents = ' '.join(preprocessed_patents) # 명사만 추출하기 전 하나의 문자열로 변환

# Extracting Nouns
hannanum = k.tag.Hannanum()
# nouns = okt.nouns(preprocessed_patents)  # komoran, kkma, okt 중 성능이 제일 좋았던 okt 적용
noun_list = []
for text in preprocessed_patent_names:
    nouns = hannanum.nouns(text)
    noun_list.append(nouns)
        
# Remove Stop Words
stop_words = ['방법', '이용', '이의', '이상', '포함', '사용자', '및', '장치', '사용', '그것', '개선', '결정', '공급',
                  '관리', '구동', '구비', '구조', '기기', '기능', '대한', '립체', '발생', '로부터'
                '용도', '조성', '형성', '용', '그', '내', '적']
cleaned_nouns = []
for words in noun_list:  # 이중 리스트의 각 내부 리스트에 대해 반복
    cleaned_words = []
    for word in words:  # 내부 리스트의 각 단어에 대해 반복
        if word not in stop_words:  # 스탑워드가 아닌 단어만 추가
            cleaned_words.append(word)
    cleaned_nouns.append(cleaned_words)
# print(nouns_clean[:40])

nouns_sentences = [' '.join(nouns) for nouns in noun_list]
# # TF-IDF 벡터화
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(nouns_sentences)

# Make Spark Session
spark = SparkSession \
        .builder \
        .master('local') \
        .appName('my_pyspark_app') \
        .getOrCreate()
        
spark.sparkContext.setLogLevel("ERROR")
        
# Make RDD
rdd = spark.sparkContext.parallelize(zip(all_patents, patents_main_sub_ipc, all_patents_dates, all_patents_applicants, all_patents_ipc_string))

# Define Schema Of The Data
schema = StructType([
    StructField("patent_name", StringType(), True),
    StructField("ipc_list", ArrayType(StringType()), True),
    StructField("application_date", StringType(), True),
    StructField("applicant", StringType(), True),
    StructField("ipc_string", StringType(), True)
])

# RDD를 DataFrame으로 변환
df = spark.createDataFrame(rdd, schema=schema)

fp_growth = FPGrowth(itemsCol="ipc_list", minSupport=0.0001, minConfidence=0.05)
model = fp_growth.fit(df)

freqItemsets = model.freqItemsets
# Obtain Association Rules based on IPC And Order by Descending
associationRules = model.associationRules.orderBy(F.col("confidence").desc())

while True:
    # Get Keyword Input
    keyword = input("검색할 키워드를 입력하세요: ")

    # Vectorize Keyword to TF-IDF
    keyword_tfidf = tfidf_vectorizer.transform([keyword])

    # Get Cosine Similarity
    similarity_matrix = cosine_similarity(tfidf_matrix, keyword_tfidf)

    # print(similarity_matrix.flatten().tolist())  # 유사도 리스트 출력

    flat_similarity = similarity_matrix.flatten().tolist()

    # Obtain The Index Of The Most Similar Patent
    target_patent_index = sorted(range(len(flat_similarity)), key=lambda i: flat_similarity[i], reverse=True)[0]
    target_ipc = patents_main_sub_ipc[target_patent_index][0]

    # print(freqItemsets.count())
    # print(associationRules.count())
    # freqItemsets.show()

    print("Target IPC:", target_ipc)

    # Filter Association Rules By Target IPC And Order By Confidence Value
    expr_string_1 = f"exists(antecedent, ipc -> array_contains(split(ipc, ' '), '{target_ipc}'))"
    filtered_rules_1 = associationRules.filter(F.expr(expr_string_1)).orderBy(F.col("confidence").desc())

    expr_string_2 = f"exists(consequent, ipc -> array_contains(split(ipc, ' '), '{target_ipc}'))"
    filtered_rules_2 = associationRules.filter(F.expr(expr_string_2)).orderBy(F.col("confidence").desc())

    filtered_rules_concat = filtered_rules_1.union(filtered_rules_2).orderBy(F.col("confidence").desc())

    filtered_rules_1.show()
    filtered_rules_2.show()
    filtered_rules_concat.show()

    # Get Antecedent, Consequent Value With the Highest, Lowest Confidence Value
    antecedent_value_highest = filtered_rules_concat.select('antecedent').collect()[0][0]
    consequent_value_highest = filtered_rules_concat.select('consequent').collect()[0][0]

    antecedent_value_lowest = filtered_rules_concat.select('antecedent').collect()[-1][0]
    consequent_value_lowest = filtered_rules_concat.select('consequent').collect()[-1][0]
              
    # Get Patent Informations Which Are Trending or Emerging Up To 3       
    patent_names_highest = df.filter(col("ipc_string")==f'{antecedent_value_highest[0]} {consequent_value_highest[0]}').select("patent_name", "application_date", "applicant") \
                    .orderBy(desc("application_date")).limit(3)

    patent_names_lowest = df.filter(col("ipc_string")==f'{antecedent_value_lowest[0]} {consequent_value_lowest[0]}').select("patent_name", "application_date",  "applicant") \
                    .orderBy(desc("application_date")).limit(3)

    # Show Obtained Patents that represents Trending, Emerging Technologies
    print("Most Trending Patents with given keywords")
    patent_names_highest.show(truncate=False)
    print("Emerging Patents with given keywords")
    patent_names_lowest.show(truncate=False)