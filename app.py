from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})


@app.route('/echo', methods=['GET'])
def echo():
    data = request.args.get('data')
    return jsonify({'data': data})

@app.route('/call', methods=['POST'])
def call_handler():
    print("\n\n------------------------------Called Received------------------------------")
    print(request.json)
    print("")
    return jsonify({'received': "OK"})

if __name__ == '__main__':
    load_dotenv()
    port = int(os.getenv('PORT')) if 'PORT' in os.environ else 80
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)