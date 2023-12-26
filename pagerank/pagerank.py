import pymongo
import networkx as nx
import json

# 连接到 MongoDB
client = pymongo.MongoClient("localhost", 27017)
db = client["Newsina"]
collection = db["newsina"]

# 创建有向图
G = nx.DiGraph()

# 从 MongoDB 读取数据并构建图
for document in collection.find():
    url = document["url"]
    page_links = document.get("page_link", [])
    
    # 确保图中包含当前页面的节点
    if not G.has_node(url):
        G.add_node(url)
    
    # 检查page_links中是否有包含"download"的元素
    # 如果有，则从MongoDB的document的page_link中删除这些元素
    links_to_remove = [link for link in page_links if "download" in link]
    if links_to_remove:
        collection.update_one(
            {"_id": document["_id"]},
            {"$pull": {"page_link": {"$in": links_to_remove}}}
        )
        # 更新当前page_links，移除包含"download"的元素
        page_links = [link for link in page_links if link not in links_to_remove]

    
    # 对于每个 page_link，添加一个从当前页面指向 page_link 的边
    for link in page_links:
        if url != link:
            if not G.has_node(link):
                G.add_node(link)
            G.add_edge(url, link)

# 应用 PageRank 算法
pagerank_scores = nx.pagerank(G)

# 将结果按分数从大到小排序
sorted_scores = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)

# 创建一个字典来存储排序后的 URL 和分数
sorted_url_scores = {url: score for url, score in sorted_scores}

# 将字典写入 JSON 文件
with open('./pagerank_scores.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_url_scores, file, ensure_ascii=False, indent=4)

print("Sorted PageRank scores saved to 'pagerank_scores.json'.")

# 读取JSON文件并更新MongoDB中的文档
with open('./pagerank_scores.json', 'r', encoding='utf-8') as file:
    pagerank_scores = json.load(file)

    # 遍历每个URL和对应的PageRank分数
    for url, score in pagerank_scores.items():
        # 如果URL在MongoDB中存在，则更新其pagerank_score
        result = collection.update_one(
            {"url": url},  # 查询条件
            {"$set": {"pagerank_score": score}}  # 更新操作
        )
        
        # 打印更新结果
        if result.matched_count:
            print(f"Updated pagerank_score for {url}")
        else:
            print(f"URL {url} not found in MongoDB")

print("MongoDB documents have been updated with PageRank scores.")