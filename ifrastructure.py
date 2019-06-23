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


async def main():
    app = Application()
    bot = Bot(app)
    api = Api(app)

    await asyncio.gather(bot.start(), api.start())


if __name__ == '__main__':
    asyncio.run(main())
