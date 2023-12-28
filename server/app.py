from flask import Flask, jsonify, request
from flask_cors import CORS
from search import search
from wildcardSearch import wildcardSearch
from phraseSearch import phraseSearch
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='server/search_logs.log', level=logging.INFO)


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
            print(text, keywords, startDate, endDate, media, excluded_content)
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
