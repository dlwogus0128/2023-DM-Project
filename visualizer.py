import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 그래프로 나타내기

def visualize_results(svd_components, tfidf_results):
    graph = nx.Graph()

    for idx, topic in enumerate(svd_components):
        topic_keywords = [(tfidf_results[i], topic[i].round(5)) for i in topic.argsort()[:-10 - 1:-1]]
        keywords = [keyword for keyword, _ in topic_keywords]
        graph.add_nodes_from(keywords)

        for i in range(len(keywords) - 1):
            for j in range(i + 1, len(keywords)):
                weight = abs(topic_keywords[i][1] - topic_keywords[j][1])  # TF-IDF 값의 차이를 이용하여 가중치 계산
                graph.add_edge(keywords[i], keywords[j], weight=weight)

    # 단어 중요도 계산해 배치 (.,.)

    centrality = nx.betweenness_centrality(graph)
    sorted_centrality = {k: v for k, v in sorted(centrality.items(), key=lambda item: item[1], reverse=False)}
    pos = {node: (centrality[node], idx) for idx, node in enumerate(sorted_centrality.keys())}

    # 폰트 설정 및 레이아웃

    font_path = "C:/Windows/Fonts/gulim.ttc"  # 원하는 폰트 경로로 수정
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(graph, k=0.1)
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color='#1B5E20')
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.3)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="#FFFFFF", font_family=font_name)
    plt.axis('off')
    plt.show()
