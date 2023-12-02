import re
import konlpy as k

# 한국어 문자만, 중복 공백 삭제
def preprocess_kor(text):
    results = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text)
    return re.sub(r"\s+", " ", results).strip()

# 명사만
def get_nouns(text_list):
    okt = k.tag.Okt()
    nouns = [noun for text in text_list for noun in okt.nouns(text)]
    return nouns

# 불용어 제거
def remove_stop_words(words, stop_words):
    return [word for word in words if word not in stop_words]
