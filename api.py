"""
Servidor aiohttp simple que recibe un post en http://vituin-chat.iaas.ull.es/api/newbadge
y lo imprime
"""
import sys,traceback
import os, base64, json, shutil
from aiohttp import web
from application import Application
import asyncio

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
            #image = await request.data()
            if self.valid_badgeClass(badge):
                new_badge = self.app.create_badge(**badge)
                if new_badge is None:
                    raise ValueError("El badge ya existe")
                path = 'api/badge/' + new_badge.uuid + '/'
                os.mkdir(path)
                with open(path + 'badge.png', 'wb') as f: #png
                    f.write(base64.b64decode(badge['image']))

                badge['image'] = 'http://vituin-chat.iaas.ull.es' + path + 'badge.png'
                badge['issuer'] = 'http://vituin-chat.iaas.ull.es/api/issuer.json'
                with open(path + 'class.json', 'w') as f: #class
                    json.dump(badge, f)

                with open(path + 'badge.html', 'w') as f: #criteria
                    for criteria in badge['criteria']:
                        f.write(criteria + '\n')

                return web.Response(text="200: OK" + new_badge.uuid)
            else:
                raise ValueError
        except Exception as error:
            shutil.rmtree(path)
            print(type(error), str(error))
            return web.HTTPBadRequest(text=str(error))

    async def badge(self, request):
        try:
            badge_id = request.match_info['badge_id']
            requested_file = request.match_info['requested_file']
            served_files = ['image', 'json', 'criteria']
            if not self.app.has_badge(badge_id) or requested_file not in served_files:
                return web.HTTPBadRequest(text="404: Not found")

            filepath = 'api/badge/' + badge_id + '/'
            if requested_file == "image":
                return web.FileResponse(filepath + 'badge.png')
            if requested_file == "json":
                return web.FileResponse(filepath + 'badge.json')
            if requested_file == "criteria":
                return web.FileResponse(filepath + 'badge.html')
        except:
            traceback.print_exc(file=sys.stdout)

    def start(self, loop):
        app = web.Application()
        app.add_routes([web.post('/api/newbadge', self.newbadge)])
        app.add_routes([web.get('/api/badge/{badge_id}/{requested_file}', self.badge)])
        web.run_app(app, port=5000)
        runner = web.AppRunner(app)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, '0.0.0.0', 5000)
        loop.run_until_complete(site.start())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = Application()
    api = Api(app)
    loop.run_until_complete(api.start(loop))

