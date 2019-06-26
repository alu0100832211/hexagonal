"""
Servidor aiohttp simple que recibe un post en http://vituin-chat.iaas.ull.es/api/newbadge
y lo imprime
"""
import sys,traceback
import os, base64, json, shutil
from aiohttp import web
from application import Application
from persistence import Persistence
from award import Award
import asyncio
import uuid
import logging
import time
from datetime import datetime

class Api:
    def __init__(self, app: Application):
        self.app = app
        self.badges = dict()
        try:
            with open('api/badges.json', 'r') as f:
                self.badges = json.load(f)
        except FileNotFoundError:
            pass



    def valid_badgeClass(self, badgeClassJson):
        keys = ["name", "description", "criteria", "image"]
        if all(key in keys for key in badgeClassJson):
            return True
        return False

    async def newbadge_handler(self, request):
        """Recibe un json con la estructura
        de un badge class
        """
        try:
            badge = await request.json()

            if self.valid_badgeClass(badge):
                ##new_badge = self.app.create_badge(**badge)
                badge_id = str(uuid.uuid4().hex)
                self.badges[badge_id] = badge['name']

                ##if new_badge is None:
                ##    raise ValueError("El badge ya existe")
                path = 'api/badge/' + badge_id + '/'
                os.makedirs(path)

                with open(path + 'badge.png', 'wb') as f: #png
                    f.write(base64.b64decode(badge['image']))

                badge['image'] = 'http://vituin-chat.iaas.ull.es/' + path + 'badge.png'
                badge['issuer'] = 'http://vituin-chat.iaas.ull.es/api/issuer.json'
                with open(path + 'badge.json', 'w') as f: #class
                    json.dump(badge, f)

                with open(path + 'badge.html', 'w') as f: #criteria
                    for criteria in badge['criteria']:
                        f.write(criteria + '\n')

                with open('api/badges.json', 'w') as f:
                    json.dump(self.badges, f)

                return web.Response(text="200: OK " + badge_id)
            else:
                raise ValueError
        except Exception as error:
            shutil.rmtree(path)
            print(type(error), str(error))
            return web.HTTPBadRequest(text=str(error))

    async def badge_handler(self, request):
        try:
            badge_id = request.match_info['badge_id']
            requested_file = request.match_info['requested_file']
            served_files = ['badge.png', 'image', 'json', 'criteria']
            #if not self.app.has_badge(badge_id) or requested_file not in served_files:
            #    return web.HTTPBadRequest(text="404: Not found")
            if requested_file not in served_files:
                return web.HTTPBadRequest(text="404: Not found")

            filepath = 'api/badge/' + badge_id + '/'
            if requested_file in ["image", "badge.png"]:
                return web.FileResponse(filepath + 'badge.png')
            if requested_file == "json":
                return web.FileResponse(filepath + 'badge.json')
            if requested_file == "criteria":
                return web.FileResponse(filepath + 'badge.html')
        except:
            traceback.print_exc(file=sys.stdout)
            return web.HTTPBadRequest()

    async def award_handler(self, request):
        try:
            filepath = 'api/award/' + award_id + '/json'
            award_id = request.match_info['award_id']
            requested_file = request.match_info['requested_file']
            if requested_file == 'json':
                return web.fileresponse(filepath + 'award.json')
        except:
            traceback.print_exc(file=sys.stdout)
            return web.HTTPBadRequest()

    async def newaward_handler(self, request):
        json_recv = await request.json()
        try:
            print(json.dumps(json_recv, indent=True))
            for badge_id2 in self.badges:
                if self.badges[badge_id2] == json_recv['name']:
                    badge_id = badge_id2
                    break
            if badge_id is None:
                raise ValueError
            badge_url = 'http://vituin-chat.iaas.ull.es/api/badge/' + badge_id + '/json'
            params = dict()
            params['id'] = uuid.uuid4().hex
            params['email'] = json_recv['email']
            params['timestamp'] = str(datetime.fromtimestamp(time.time()))
            params['badge_url'] = badge_url
            award = Award(**params)

            print(json.dumps(award.json, indent=True))

            return web.Response(text="200: OK")
        except:
            traceback.print_exc(file=sys.stdout)
            return web.HTTPBadRequest()

    async def awards_handler(self, request):
        filepath = 'api/awards.json'
        return web.FileResponse(filepath)

    async def badges_handler(self, request):
        filepath = 'api/badges.json'
        return web.FileResponse(filepath)

    async def issuer_handler(self, request):
        filepath = 'api/issuer.json'
        return web.FileResponse(filepath)

    def start(self, loop=None):
        app = web.Application()
        app.router.add_post('/api/newbadge', self.newbadge_handler)
        app.router.add_post('/api/newaward', self.newaward_handler)
        app.router.add_get('/api/badges', self.badges_handler)
        app.router.add_get('/api/awards', self.awards_handler)
        app.router.add_get('/api/badge/{badge_id}/{requested_file}', self.badge_handler)
        app.router.add_get('/api/award/{award_id}/{requested_file}', self.award_handler)
        app.router.add_get('/api/issuer.json', self.issuer_handler)

        web.run_app(app, port=5000)

        #runner = web.AppRunner(app)
        #loop.run_until_complete(runner.setup())
        #site = web.TCPSite(runner, '0.0.0.0', 5000)
        #loop.run_until_complete(site.start())

if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    logging.basicConfig(level=logging.DEBUG)
    api = Api(None)
    api.start()
    #loop.run_until_complete(api.start(loop))

