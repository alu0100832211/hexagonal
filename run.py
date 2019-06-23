"""
desde este fichero se llama a todos los demas
1. Persistencia
2. Bot
3. ???
"""


from bot import *
from application import Application
from config import Config

app = Application()
config = Config()

def recuperar_entidades():
# Recuperar issuer
# Recuperar personas
# Recuperar badges
# Recuperar awards
    app.config = config
#    try:
#        with open(badges_path()) as f:
#            badge_ids = json.load(f)
#            app.badges = list()
#            for badge_id in badge_ids:
#                with open(badge_path(badge_id=badge_id)) as f:
#                    app.badges.append(Badge(json.load(f)))
#            with open(app.config.PERSONS, 'r') as f:
#                app.persons = json.load(f)["persons"]
#                for person_id in app.persons:
#                    filename = app.config.person + person_id + '.json'
#                    app.person = dict()
#                    with open(filename, 'r') as f:
#                        app.person[person_id] = json.load(f)
#            with open(app.config.AWARDS, 'r') as f:
#                app.awards = json.load(f)["awards"]
#                for award_id in app.awards:
#                    filename = app.config.award + award_id + '.json'
#                    app.award = dict()
#                    with open(filename, 'r') as f:
#                        app.award[award_id] = json.load(f)
#            with open(app.config.issuer, 'r') as f:
#                app.issuer = json.load(f)["issuer"]
#
#    except Exception as error:
#        sys.exit(str(error))



def iniciar_bot():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()

def main():
    recuperar_entidades()
    iniciar_bot()

