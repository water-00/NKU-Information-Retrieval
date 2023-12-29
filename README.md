[Scrapy  新浪新闻爬虫](https://zhuanlan.zhihu.com/p/71925619)


相关链接的class:
ty-card ty-card-type1 clearfix

通配查询使用例子：
- 先搜索"融"，得到结果
- 再打开通配查询，搜索"?融"，就能得到金融相关的页面
- 搜索国、?国、??国也能说明

# 1. 从 Elasticsearch 获取新闻数据。
# 2. 使用 TF-IDF 向量化新闻内容。
# 3. 对于指定的新闻，计算它与数据库中其他新闻的相似度。
# 4. 选择相似度最高的五篇新闻作为推荐。