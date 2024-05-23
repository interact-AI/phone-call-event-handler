from flask import Flask, jsonify, request
from dotenv import load_dotenv
from azure.communication.callautomation import (
    CallAutomationClient
)
from azure.communication.callautomation import FileSource

print("Setting up azure communication services...")
app = Flask(__name__)
endpoint_url = 'endpoint=https://voicecallresource.brazil.communication.azure.com/;accesskey=Es26fVjrw3z3vGBQq0lqo4HDlH9QwMqie4mIv2v2VHaKBFzoaXaeM2ljhk68PIqtuB+hl4J2r9GEravehdJGvw=='
callback_url = "https://incomingcall-python-api.azurewebsites.net/call"
client = CallAutomationClient.from_connection_string(endpoint_url)
my_file = FileSource(url="https://interactaidata.blob.core.windows.net/test/audio.wav")


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
    call_context = request.json[0]["data"]["incomingCallContext"]
    print("Call Context: ", call_context)
    result = client.answer_call(incoming_call_context=call_context, callback_url=callback_url)    
    call_connection_id = result.call_connection_id
    call_connection = client.get_call_connection(call_connection_id)
    print("Start audio file...")
    call_connection.play_media(my_file)
    print("End call")
    return jsonify({'received': "OK"})


load_dotenv()
port = 8000
print(f"Server running on port {port}")
app.run(host='0.0.0.0', port=port)