"""
Servidor aiohttp simple que recibe un post en http://vituin-chat.iaas.ull.es/api/newbadge
y lo imprime
"""
from aiohttp import web
from application import Application

class Api:
    def __init__(self, app: Application):
        self.app = app

    def valid_badgeClass(self, badgeClassJson):
        keys = ["name", "description", "criteria", "image"]
        if all(key in keys for key in badgeClassJson):
            return True
        return False

    async def newbadge(self, request):
        """Recibe un json con la estructura
        de un badge class
        """
        try:
            badge = await request.json()
            if self.valid_badgeClass(badge):
                print(badge)
                self.app.create_badge(**badge)
                return web.Response(text="200: OK")
            else:
                raise Exception
        except Exception as error:
            return web.HTTPBadRequest(text=str(error))

    async def start(self):
        app = web.Application()
        app.add_routes([web.post('/api/newbadge', self.newbadge)])
        web.run_app(app, port=5000)


if __name__ == '__main__':
    app = Application()
    api = Api(app)
    api.start()
