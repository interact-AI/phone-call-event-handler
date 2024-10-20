import os
from aiohttp import web
from http import HTTPStatus
from aiohttp.web import Request, Response
import ssl
from azure.communication.callautomation import CallAutomationClient, FileSource
import asyncio
from dotenv import load_dotenv

print("Creating call automation client...")
load_dotenv()
acs_conn_str = os.getenv("ACS_CONNECTION_STRING")
call_automation_client = CallAutomationClient.from_connection_string(
    acs_conn_str)


async def handle_pki_validation(request):
    file_path = './.well-known/pki-validation/BDD3B7F42D29EB9BE715EE3E1CF6C922.txt'
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    else:
        return web.Response(text="File not found", status=404)


async def status(req: Request) -> Response:
    print("Received status request")
    return Response(status=HTTPStatus.OK, text="Healthy")


async def postInfo(req: Request) -> Response:
    print("\nReceived info")
    body = await req.json()
    print("Answering call...")
    try:
        incoming_call_context = body[0]["data"]["incomingCallContext"]
        call_automation_client.answer_call(
            incoming_call_context=incoming_call_context, callback_url="https://20.122.16.133:80/acs-callback"
        )
    except Exception as e:
        print(e)
        return Response(status=HTTPStatus.OK, text="Error answering call")
    print("Call answered successfully")
    return Response(status=HTTPStatus.OK)


async def acs_callback(req: Request) -> Response:
    body = await req.json()
    body = body[0]
    print("\nReceived ACS callback")
    event_type = body['type']

    if event_type == 'Microsoft.Communication.CallConnected':
        call_connection_id = body['data']['callConnectionId']
        print("Call connected.\nPlaying media...")

        my_file = FileSource(
            url="https://firebasestorage.googleapis.com/v0/b/stella-app-8ad37.appspot.com/o/buenas.mp3?alt=media&token=31cc6235-33fa-4f54-b691-06fb19306fc4"
        )

        call_connection = call_automation_client.get_call_connection(
            call_connection_id)
        try:
            call_connection.play_media_to_all(my_file)
            print("Media played successfully")
        except Exception as e:
            print(e)
    else:
        print(f"Event type {event_type} not supported\nExiting... ")
    return Response(status=HTTPStatus.OK)

app = web.Application()
app.router.add_get(
    '/.well-known/pki-validation/BDD3B7F42D29EB9BE715EE3E1CF6C922.txt', handle_pki_validation)
app.router.add_get("/status", status)
app.router.add_post("/info", postInfo)
app.router.add_post("/acs-callback", acs_callback)

if __name__ == "__main__":
    cert_path = './certificate.crt'
    key_path = './private.key'

    # Create SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    web.run_app(app, host="0.0.0.0", port=80, ssl_context=ssl_context)
