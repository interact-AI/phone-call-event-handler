from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests

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
    if isinstance(request.json, list) and 'validationUrl' in request.json[0]:
        print("\n\n------------------------------Validation Request------------------------------")
        print("Making request to validate...")
        response = requests.get(request.json[0]['validationUrl'])
        print("Validation request received. Response:")
        print(response.text)
        print("")
        return jsonify({'validationUrlExitCode': response.status_code})
    print("\n\n------------------------------Called Received------------------------------")
    print(request.json)
    print("")
    
    return jsonify({'received': "OK"})

    
    
    


    return jsonify({'received': "OK"})

if __name__ == '__main__':
    load_dotenv()
    port = int(os.getenv('PORT')) if 'PORT' in os.environ else 80
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)