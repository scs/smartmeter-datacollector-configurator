import logging

from aiohttp import web


DEFAULT_STATIC_DIR_PATH = "../frontend/dist"

logging.basicConfig(level=logging.DEBUG)

routes = web.RouteTableDef()

# Routes
@routes.get('/api/config')
async def get_config(request):
    data = {'todo': "TODO"}
    return web.json_response(data)


@routes.post('/api/config')
async def post_config(request):
    return web.Response(text="TODO")


@routes.post('/api/restart')
async def post_restart(request):
    return web.Response(text="TODO")


@routes.put('/api/reset_password')
async def put_reset_password(request):
    return web.Response(text="TODO")

routes.static('/', DEFAULT_STATIC_DIR_PATH, show_index=True)



def make_app():
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(make_app())
