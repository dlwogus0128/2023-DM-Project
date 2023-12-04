import json
from preprocessor import *
from LSA import *
from visualizer import *

def main():
    # json 파일 불러오기
    patent_file_path = "patent.json"
    with open(patent_file_path, "r", encoding="utf-8") as file:
        patent_data = json.load(file)
    
    # 특허 이름 추출
    all_patents = []
    for data in patent_data:
        patents = data["patents"]
        patent_names = [patent["patent_name"] for patent in patents]
        all_patents.extend(patent_names)

    ### 텍스트 전처리 ###
    preprocessed_patents = [preprocess_kor(name) for name in all_patents]

    # 형태소 분석 및 불용어 처리
    stop_words = ['방법', '이용', '이의', '이상', '포함', '사용자', '및', '장치', '사용', '함유', '그것', '개선', '검사', '결정', '공급',
                  '관리', '구동', '구비', '구조', '기기', '기능', '기록', '기반', '다중', '단말', '대한', '동작', '디바이스', '립체', '매체', '모듈', '물질', '발생',
                  '방지', '보호', '복합', '부품', '분석', '분리', '생산', '서비스', '시스템', '용도', '유닛', '제공', '조성', '처리', '표시', '향상', '형성']
    nouns = get_nouns(preprocessed_patents)
    nouns_clean = remove_stop_words(nouns, stop_words)
    
    ####################

    # TF-IDF 수행
    X_tfidf, tfidf_results = perform_tfidf(nouns_clean)

    # 특이값 분해
    svd_model = truncated_svd(X_tfidf)

    # 결과 출력
    get_lsa_results(svd_model.components_, tfidf_results)

    # 결과 시각화
    visualize_results(svd_model.components_, tfidf_results)

if __name__ == "__main__":
    main()
