import os
from aiohttp import web
from http import HTTPStatus
from aiohttp.web import Request, Response

async def handle_pki_validation(request):
    file_path = './.well-known/pki-validation/38396ED348AFD2CCBC953C4F798FDBFF.txt'
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
app.router.add_get('/.well-known/pki-validation/38396ED348AFD2CCBC953C4F798FDBFF.txt', handle_pki_validation)
app.router.add_get("/status", status)
app.router.add_post("/info", postInfo)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=80)
