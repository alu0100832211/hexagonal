# Problema 1: Cuanod se borra algo en api/ no lo refleja el programa
"""
Servidor aiohttp simple que recibe un post en http://vituin-chat.iaas.ull.es/api/newbadge
y lo imprime
"""
import sys,traceback
import os, base64, json, shutil
from aiohttp import web
import aiohttp
import aiofiles
from application import Application
from persistence import Persistence
from award import Award
from config import Config
import asyncio
import uuid
import logging
import time
from datetime import datetime

class Api:
    def __init__(self, app: Application):
        self.config = Config()
        self.api_path = self.config.api_path
        self.bakery_path = 'https://backpack.openbadges.org/baker?assertion='
        self.app = app
        self.awards = dict()
        self.badges = dict()
        try:
            with open('api/badges.json', 'r') as f:
                self.badges = json.load(f)
            with open('api/awards.json', 'r') as f:
                self.awards = json.load(f)
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
                self.badges[badge_id] = dict()
                self.badges[badge_id]['name'] = badge['name']
                self.badges[badge_id]['url'] = f"{self.api_path}/badge/{badge_id}/json"


                ##if new_badge is None:
                ##    raise ValueError("El badge ya existe")
                path = 'api/badge/' + badge_id + '/'
                os.makedirs(path)

                with open(path + 'badge.png', 'wb') as f: #png
                    f.write(base64.b64decode(badge['image']))

                with open(path + 'badge.html', 'w') as f: #criteria
                    for criteria in badge['criteria']:
                        f.write(criteria + '\n')
                badge['image'] = f"{self.api_path}/badge/{badge_id}/image"
                badge['issuer'] = f"{self.api_path}/issuer"
                badge['criteria'] = f"{self.api_path}/badge/{badge_id}/criteria"
                with open(path + 'badge.json', 'w') as f: #class
                    json.dump(badge, f)


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
        except FileNotFoundError:
            return web.HTTPBadRequest(text="404: Not found")
        except Exception as error:
            print(type(error))
            #traceback.print_exc(file=sys.stdout)
            return web.HTTPBadRequest()

    async def award_handler(self, request):
        try:
            award_id = request.match_info['award_id']
            requested_file = request.match_info['requested_file']
            filepath = f"api/award/{award_id}"
            if requested_file == 'json':
                return web.FileResponse(f"api/award/{award_id}/award.json")
            if requested_file == 'image':
                return web.FileResponse(f"api/award/{award_id}/award.png")
        except:
            traceback.print_exc(file=sys.stdout)
            return web.HTTPBadRequest()

    async def bake_award(self, award_id):
        #r = await requests.get(bake_api_request, stream=True) #stream=True so that requests doesn't download the whole image into memory first.
        async with aiohttp.ClientSession() as session:
            url = f"{self.bakery_path}{self.api_path}/award/{award_id}/json"
            print(f"getting {url}...")
            async with session.get(url) as resp:
                if resp.status == 200:
                    print(f"writing {award_id}/award.png")
                    f = await aiofiles.open(f"api/award/{award_id}/award.png", mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                else:
                    print(f"error: {await resp.read()}")
                    sys.exit()
                print(f"written!")


    async def newaward_handler(self, request):
        json_recv = await request.json()
        try:
            print(json.dumps(json_recv, indent=True))
            print(self.badges)
            badge_id = None
            for badge_id2 in self.badges:
                if self.badges[badge_id2]['name'] == json_recv['name']:
                    badge_id = badge_id2
                    break
            if badge_id is None:
                raise ValueError
            badge_url = f"{self.api_path}/badge/{badge_id}/json"
            params = dict()
            params['id'] = uuid.uuid4().hex
            params['email'] = json_recv['email']
            params['timestamp'] = str(datetime.utcnow().isoformat())
            params['badge_url'] = badge_url
            award = Award(**params)

            award_path = f"api/award/{award.id}/award.json"
            os.makedirs(f"api/award/{award.id}/")
            with open(award_path, 'w') as f:
                json.dump(award.json, f)

            self.awards[award.id] = {
                    'name': json_recv['name'] + " to " + json_recv['email'],
                    'url': f"{self.api_path}/award/{award.id}/json"
                    }
            with open("api/awards.json", 'w') as f:
                json.dump(self.awards, f)

            await self.bake_award(award.id)

            return web.Response(text=award.id)
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
        app.router.add_get('/api/issuer', self.issuer_handler)

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

