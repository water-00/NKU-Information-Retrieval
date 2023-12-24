from elasticsearch import Elasticsearch
import pymongo

# 连接到Elasticsearch
USERNAME = "elastic"
PASSWORD = "aYJ-U7SNLSE4X=ZnosE3"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

# 连接到MongoDB
client = pymongo.MongoClient("localhost", 27017)
db = client["Newsina"]
collection = db["newsina"]

# 设置Elasticsearch索引的映射和配置
settings = {
    "index": {
        "number_of_replicas": 2,
        "number_of_shards": 1
    },
    "analysis": {
        "filter": {
            "autocomplete_filter": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20
            }
        },
        "analyzer": {
            "autocomplete": {  # 自动补全分析器
                "type": "custom",
                "tokenizer": "ik_smart",
                "filter": [
                    "lowercase",
                    "autocomplete_filter"
                ]
            },
            "ik_max_word_analyzer": {
                "type": "custom",
                "tokenizer": "ik_max_word",
                "filter": ["lowercase"]
            }
        }
    }
}

mappings = {
    "properties": {
        "ctime": {"type": "date", "format": "yyyy-MM-dd HH:mm"},
        "url": {"type": "keyword"},
        "wapurl": {"type": "keyword"},
        "title": {
            "type": "text",
            "analyzer": "ik_max_word",
            "fields": {
                "autocomplete": {  # 为标题添加自动补全字段
                    "type": "text",
                    "analyzer": "autocomplete"
                }
            }
        },
        "media_name": {"type": "keyword"},
        "keywords": {"type": "text", "analyzer": "ik_max_word"},
        "content": {"type": "text", "analyzer": "ik_max_word"}
    }
}


# 创建Elasticsearch索引（如果不存在）
index_name = "newsina_index"
if es.indices.exists(index=index_name):
    es.options(ignore_status=404).indices.delete(index=index_name)
es.indices.create(
    index=index_name,
    body={
        "settings": settings,
        "mappings": mappings
    }
)

# 遍历 MongoDB 集合并索引数据到 Elasticsearch
for doc in collection.find():
    doc_id = str(doc['_id'])
    del doc['_id']
    # 索引文档到 Elasticsearch
    es.index(index=index_name, id=doc_id, body=doc)

    content = doc.get("content", "")
    
    # # 检查 content 是否为空
    # if content:
    #     # 使用 _analyze API 分析文本
    #     analyze_body = {
    #         "analyzer": "ik_max_word",
    #         "text": content
    #     }

    #     response = es.indices.analyze(body=analyze_body)
    #     print("Analyze Result:", response)
    #     print("\n")