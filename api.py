"""
Servidor aiohttp simple que recibe un post en http://vituin-chat.iaas.ull.es/api/newbadge
y lo imprime
"""
from aiohttp import web
from application import Application

class Api:
    def __init__(app: Application):
        self.app = app

    routes = web.RouteTableDef()

    def validate_badgeClass(self, badgeClassJson):
        keys = ["name", "description", "criteria", "image"]
        if all(key in keys for key in badgeClassJson):
            return True
        return False

    @routes.post('/api/newbadge')
    async def newbadge(self, request):
        """Recibe un json con la estructura
        de un badge class
        """
        try:
            badge = await request.json()
            if valid_badgeClass(badge):
                self.app.new_badge(**badge)
                return web.Response(text="200: OK")
            else:
                raise Exception
        except Exception as error:
            return web.HTTPBadRequest()

    def start(self):
        app = web.Application()
        app.add_routes(routes)
        web.run_app(app, port=5000)
