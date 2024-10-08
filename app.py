import os
from aiohttp import web
from http import HTTPStatus
from aiohttp.web import Request, Response
import ssl


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
