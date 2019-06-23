"""Este fichero junta los tres componentes de la infraestructura
1. Bot
2. API
3. Persistencia
"""
from bot import Bot
from api import Api
from persinstence import Persistence
from application import Application


def main(argv):
    app = Application()

    #bot = Bot(app)
    api = Api(app)

    #bot.start()
    api.start()

if __name__ == '__main__':
    main(sys.argv)
