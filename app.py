from flask import Flask, jsonify, request


print("Setting up api...")
app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})


@app.route('/echo', methods=['GET'])
def echo():
    data = request.args.get('data')
    return jsonify({'data': data})

port = 80
print(f"Server running on port {port}")

app.run(host='0.0.0.0', port=port)