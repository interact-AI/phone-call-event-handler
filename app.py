import os
from aiohttp import web

async def handle_pki_validation(request):
    file_path = './.well-known/pki-validation/38396ED348AFD2CCBC953C4F798FDBFF.txt'
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    else:
        return web.Response(text="File not found", status=404)

app = web.Application()
app.router.add_get('/.well-known/pki-validation/38396ED348AFD2CCBC953C4F798FDBFF.txt', handle_pki_validation)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
