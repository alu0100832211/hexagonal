"""Este fichero junta los tres componentes de la infraestructura
1. Bot
2. API
3. Persistencia
"""
from bot import Bot
from api import Api
#from persinstence import Persistence
from application import Application
import asyncio


async def main(loop):
    app = Application()
    bot = Bot(app)
    api = Api(app)
    await bot.start(loop)
    await api.start(loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
