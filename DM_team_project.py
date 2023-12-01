import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np

patent_file_path = "patent.json"

with open(patent_file_path, "r", encoding="utf-8") as file:
    patent_data = json.load(file)

patent_names = [patent["patent_name"] for patent in patent_data[0]["patents"]]

#1. 데이터 전처리 수행 (한국어 문자 및 공백만 남도록)

def preprocess_text(text):
    results = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text) # 한국어 문자에 관해서만 ~.~
    results = re.sub(r"\s+", " ", results).strip() # 중복 공백 제거
    return results

preprocessed_patents = [preprocess_text(name) for name in patent_names]

# 3. TF-IDF 적용
vectorizer = TfidfVectorizer(max_features=10)
X_tfidf = vectorizer.fit_transform(preprocessed_patents)

print(vectorizer.get_feature_names_out())

#정수 인덱스의 이름 불러오기
# print(vectorizer.get_feature_names_out())

# #3. SVD 적용 

# svd = TruncatedSVD(n_components=2)
# svd_result = svd.fit_transform(X_tfidf)

# # TF-IDF와 SVD 결과를 출력합니다.
# print("TF-IDF 결과:")
# print(X_tfidf)
# print("\nSVD 결과:")
# print(svd_result)

# # 3. SVD 적용
# svd = TruncatedSVD(n_components=5)
# svd_result = svd.fit_transform(X_tfidf)

# # TF-IDF와 SVD 결과를 출력합니다.
# print("\nSVD 결과:")
# print(svd_result)

# # SVD 결과를 이용하여 상위 10개의 키워드를 확인합니다.
# svd_feature_names = [f"SVD_feature_{i}" for i in range(svd_result.shape[1])]
# svd_dense_matrix = svd_result
# svd_total_tfidf_per_feature = np.sum(svd_dense_matrix, axis=0)
# svd_top_indices = svd_total_tfidf_per_feature.argsort()[-10:][::-1]

# # SVD 결과를 이용하여 상위 10개의 키워드를 확인합니다.
# for i in range(svd_result.shape[1]):
#     component_feature = svd_result[:, i]
    
#     # Select top 10 indices
#     top_keyword_indices = component_feature.argsort()[-10:][::-1]
    
#     # Ensure that the length of top_keyword_indices does not exceed the length of feature_names
#     valid_indices = top_keyword_indices[top_keyword_indices < len(feature_names)]
    
#     # Select top keywords and their corresponding weights
#     top_keywords = [(feature_names[idx], component_feature[idx]) for idx in valid_indices]
    
#     print(f"\nTop 10 Keywords from SVD_feature_{i}:")
#     for keyword, svd_value in top_keywords:
#         print(f"{keyword}: {svd_value}")