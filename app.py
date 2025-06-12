from flask import Flask, jsonify, request
from game import *
app = Flask(__name__)



@app.route('/expressions', methods=['GET'])
def get_expressions():
    num_cnt = int(request.args.get('num_cnt', 4))
    level = int(request.args.get('level', 2))

    expr = generate(num_cnt, level)
    return jsonify({'expression': expr})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')