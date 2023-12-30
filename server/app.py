import webbrowser
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from search import search
from wildcardSearch import wildcardSearch
from phraseSearch import phraseSearch
import logging
from elasticsearch import Elasticsearch

# 连接到Elasticsearch
USERNAME = "elastic"
PASSWORD = "aYJ-U7SNLSE4X=ZnosE3"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='./search_logs.log', level=logging.INFO)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345678"

@app.route('/login', methods=['POST'])
def login():
    # 获取JSON数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(username, password)

    # 校验用户名和密码
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # 登录成功，返回成功消息
        return jsonify({'message': 'Login successful'}), 200
    else:
        # 登录失败，返回错误消息
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/open-snapshot', methods=['GET'])
def open_snapshot():
    image_name = request.args.get('image_name', '')
    
    if image_name:
        # 构建图片的完整文件路径
        image_path = './resized_snapshot_img/' + image_name + '.png'
        
        # 打开图片
        try:
            webbrowser.open('file://' + os.path.abspath(image_path))
            return jsonify({'message': f'Snapshot opened for {image_name}'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No image name provided'}), 400

@app.route('/get-recommendations', methods=['GET'])
def get_recommendations():
    news_id = request.args.get('id', '')

    print("news_id: ", news_id)
    if not news_id:
        return jsonify({'error': 'No news ID provided'}), 400

    try:
        # 查询 Elasticsearch 获取推荐新闻
        res = es.get(index='newsina_index', id=news_id)
        print("res: ", res)
        if res['found']:
            # 直接访问 '_source' 中的 'recommend' 字段，它已经是一个列表了
            recommendations = res['_source'].get('recommend', [])
            return jsonify({'recommendations': recommendations})
        else:
            return jsonify({'error': 'News not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def movies():
    text = request.args.get('q', '')
    wildcard = request.args.get('wildcard', 'false') == 'true'
    phrase = request.args.get('phrase', 'false') == 'true'

    if text:
        if phrase:
            # 直接获取短语搜索的参数
            keywords = request.args.get('keywords', '')
            startDate = request.args.get('startDate', '')
            endDate = request.args.get('endDate', '')
            media = request.args.get('media', '')
            excluded_content = request.args.get('excludedContent', '')
            # print(text, keywords, startDate, endDate, media, excluded_content)
            # 短语搜索
            result = phraseSearch(text, keywords, startDate, endDate, media, excluded_content)
        elif wildcard:
            # 通配符搜索
            result = wildcardSearch(text)
        else:
            # 标准搜索
            result = search(text)
        
        # 记录日志
        log_data = {
            'text': text,
            'keywords': keywords if phrase else '',
            'startDate': startDate if phrase else '',
            'endDate': endDate if phrase else '',
            'media': media if phrase else '',
            'excluded_content': excluded_content if phrase else '',
            'result': [{'url': hit['_source']['url'], 'title': hit['_source']['title']} for hit in result['hits']['hits']]
        }
        logging.info(log_data)
        # 检查 result 是否为预期格式
        if 'hits' not in result or 'hits' not in result['hits']:
            return jsonify({'error': 'Invalid search results format'}), 500
        return jsonify(result['hits']['hits'])
    else:
        return jsonify({'error': 'No query provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
