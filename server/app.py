from flask import Flask, jsonify, request
from flask_cors import CORS
from search import search
from wildcardSearch import wildcardSearch  # 确保你已经创建了这个文件和函数


app = Flask(__name__)
CORS(app)

import sys

sys.path.append('')


@app.route('/', methods=['GET'])
def index():
    return jsonify('hahah')


@app.route('/search', methods=['GET', 'POST'])
def movies():
    text = request.args.get('q', '')
    wildcard = request.args.get('wildcard', 'false') == 'true'  # 获取通配符参数
    
    if text:
        if wildcard:
            # 如果是通配符搜索
            result = wildcardSearch(text)
        else:
            # 如果是标准搜索
            result = search(text)
        return jsonify(result['hits']['hits'])
    else:
        return jsonify('none')

if __name__ == "__main__":
    app.run(debug=True)
