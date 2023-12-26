from elasticsearch import Elasticsearch

USERNAME = "elastic"
PASSWORD = "aYJ-U7SNLSE4X=ZnosE3"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "newsina_index"

def phraseSearch(text, keywords, date, media, excluded_content):
    4