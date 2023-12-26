from elasticsearch import Elasticsearch

USERNAME = "elastic"
PASSWORD = "aYJ-U7SNLSE4X=ZnosE3"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "newsina_index"

def wildcardSearch(query: str):
    dsl = {
        "query": {
            "bool": {
                "should": [
                    {
                        "wildcard": {
                            "title": {
                                "value": f"*{query}*"
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "keywords": {
                                "value": f"*{query}*"
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "content": {
                                "value": f"*{query}*"
                            }
                        }
                    }
                ],
                "minimum_should_match": 1
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

# 可以在这里测试通配查询的功能
if __name__ == "__main__":
    print(wildcardSearch("测试"))
