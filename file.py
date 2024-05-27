from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

@app.route('/.well-known/pki-validation')
def download_file():
    return send_from_directory('.', '6C08CFC5359B7EF85313707A08B2EB5F.txt', as_attachment=True)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)