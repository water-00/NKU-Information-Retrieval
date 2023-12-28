from elasticsearch import Elasticsearch

USERNAME = "elastic"
PASSWORD = "aYJ-U7SNLSE4X=ZnosE3"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "newsina_index"

# ...其他代码...

def search(query: str):
    dsl = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "keywords", "content"],
                            "type": "best_fields",
                            "analyzer": "ik_smart",  # 使用 ik_smart 分词器
                            "tie_breaker": 0.3
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "keywords", "content"],
                            "type": "phrase",
                            "analyzer": "ik_max_word"  # 使用 ik_max_word 分词器进行短语搜索
                        }
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "title": {},
                "keywords": {},
                "content": {}
            },
            "require_field_match": False,
            "pre_tags": ["<highlight>"],
            "post_tags": ["</highlight>"]
        }
    }

    result = es.search(index=index_name, body=dsl, size=10)
    return result