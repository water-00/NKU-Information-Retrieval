from flask import Flask, jsonify, request
from flask_cors import CORS
# 以下导入假设您已经定义了相应的搜索函数
from search import search
from wildcardSearch import wildcardSearch
from phraseSearch import phraseSearch

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def movies():
    text = request.args.get('q', '')
    wildcard = request.args.get('wildcard', 'false') == 'true'
    phrase = request.args.get('phrase', 'false') == 'true'

    if text:
        if phrase:
            # 直接获取短语搜索的参数
            keywords = request.args.get('keywords', '')
            date = request.args.get('dateRange', '')
            media = request.args.get('media', '')
            excluded_content = request.args.get('excludedContent', '')
            # 短语搜索
            result = phraseSearch(text, keywords, date, media, excluded_content)
        elif wildcard:
            # 通配符搜索
            result = wildcardSearch(text)
        else:
            # 标准搜索
            result = search(text)

        # 检查 result 是否为预期格式
        if 'hits' not in result or 'hits' not in result['hits']:
            return jsonify({'error': 'Invalid search results format'}), 500
        return jsonify(result['hits']['hits'])
    else:
        return jsonify({'error': 'No query provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
