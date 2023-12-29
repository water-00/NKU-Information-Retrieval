from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from jieba import lcut
import numpy as np
import pymongo

# 连接到 Elasticsearch
USERNAME = "elastic"
PASSWORD = "aYJ-U7SNLSE4X=ZnosE3"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

# 连接到 MongoDB
client = pymongo.MongoClient("localhost", 27017)
db = client["Newsina"]
collection = db["newsina"]

# 读取中文停用词
with open('cn_stopwords.txt', 'r', encoding='utf-8') as file:
    stopwords = set([line.strip() for line in file])

# 中文文本预处理，包括分词和去除停用词
def preprocess_text(text):
    words = lcut(text)
    words = [word for word in words if word not in stopwords]
    return ' '.join(words)

# 从 MongoDB 获取新闻数据并预处理
def fetch_news_data_from_mongodb(collection):
    print("开始从 MongoDB 中提取新闻数据...")
    news_data = []
    news_info = []  # 用于保存 MongoDB 中的文档ID、标题和URL
    for document in collection.find():
        text = f"{document['title']} {document['content']}"
        preprocessed_text = preprocess_text(text)
        news_data.append(preprocessed_text)
        news_info.append({
            "_id": document['_id'],
            "title": document['title'],
            "url": document['url']
        })
    print("新闻数据提取完成。")
    return news_data, news_info

# 更新 MongoDB 文档的推荐结果
def update_recommendations_in_mongodb(collection, news_info, recommendations):
    print("开始更新 MongoDB 中的推荐结果...")
    for i, recs in enumerate(recommendations):
        rec_documents = [{'title': news_info[index]['title'], 'url': news_info[index]['url']} for index in recs]
        collection.update_one(
            {'_id': news_info[i]['_id']},
            {'$set': {'recommend': rec_documents}}
        )
    print("MongoDB 更新完成。")

# 主函数
def main():
    news_data, news_info = fetch_news_data_from_mongodb(collection)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(news_data)

    # 存储所有新闻的推荐结果
    all_recommendations = []

    print("开始进行新闻推荐...")
    for i in range(len(news_data)):
        cosine_similarities = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix).flatten()
        similar_indices = np.argsort(cosine_similarities)[-6:-1][::-1]
        all_recommendations.append(similar_indices)
        if i % 100 == 0:
            print(f"已处理 {i + 1} / {len(news_data)} 条新闻...")

    update_recommendations_in_mongodb(collection, news_info, all_recommendations)

# 执行主函数
main()
