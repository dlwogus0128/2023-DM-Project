from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def perform_tfidf(text_list, max_features=100):
    detokenized_text = ' '.join(text_list)
    vectorizer = TfidfVectorizer(max_features=max_features)
    X_tfidf = vectorizer.fit_transform([detokenized_text])
    tfidf_results = vectorizer.get_feature_names_out()
    return X_tfidf, tfidf_results

def truncated_svd(X_tfidf, n_components=20):
    svd_model = TruncatedSVD(n_components=n_components, algorithm='randomized', n_iter=100, random_state=122)
    svd_model.fit(X_tfidf)
    return svd_model

def get_lsa_results(components, feature_names, n=10):
    results = [(feature_names[i], components[0][i].round(5)) for i in components[0].argsort()[:-n - 1:-1]]
    print(results)