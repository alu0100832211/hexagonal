"""
Servidor aiohttp simple que recibe un post en http://vituin-chat.iaas.ull.es/api/newbadge
y lo imprime
"""
from aiohttp import web

routes = web.RouteTableDef()

@routes.post('/api/newbadge')
async def newbadge(request):
    return web.Response(request.text)

def init_func(argv):
    app = web.Application()
    app.add_routes(routes)
    return app
