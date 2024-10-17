import os
from aiohttp import web
from http import HTTPStatus
from aiohttp.web import Request, Response
import ssl
from azure.communication.callautomation import CallAutomationClient, FileSource
import asyncio

print("Creating call automation client...")
acs_conn_str = os.getenv("ACS_CONNECTION_STRING")
call_automation_client = CallAutomationClient.from_connection_string(
    acs_conn_str)


async def handle_pki_validation(request):
    file_path = './.well-known/pki-validation/D9C5AF9351D746285DD8204D9966211D.txt'
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    else:
        return web.Response(text="File not found", status=404)


async def status(req: Request) -> Response:
    print("Received status request")
    return Response(status=HTTPStatus.OK, text="Healthy")


async def postInfo(req: Request) -> Response:
    print("Received info")
    body = await req.json()
    print(body)
    print("Answering call...")
    incoming_call_context = body["data"]["incomingCallContext"]
    print(incoming_call_context)
    call_connection_properties = call_automation_client.answer_call(
        incoming_call_context=incoming_call_context, callback_url="https://www.google.com"
    )
    print("Getting audio file...")
    my_file = FileSource(url="./buenas.mp3")
    print("Getting call connection...")
    call_connection = call_automation_client.get_call_connection(
        call_connection_id=call_connection_properties.call_connection_id)
    print("Playing media...")
    call_connection.play_media_to_all(my_file)
    print("Waiting for 5 seconds...")
    await asyncio.sleep(5)
    print("Hanging up...")
    call_connection.hang_up(is_for_everyone=True)
    return Response(status=HTTPStatus.OK)

app = web.Application()
app.router.add_get(
    '/.well-known/pki-validation/D9C5AF9351D746285DD8204D9966211D.txt', handle_pki_validation)
app.router.add_get("/status", status)
app.router.add_post("/info", postInfo)

if __name__ == "__main__":
    cert_path = './certificate.crt'
    key_path = './private.key'

    # Create SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    web.run_app(app, host="0.0.0.0", port=80, ssl_context=ssl_context)
