from uuid import UUID
class Award:
    def __init__ (self, id, email, timestamp, badge_url):
        self.json = {
                "uid": id,
                "recipient": {
                    "type": "email",
                    "identity": email,
                    "hashed": False
                    },
                "issuedOn":  timestamp,
                "badge": badge_url,
                "verify": {
                    "type": "hosted",
                    "url": 'http://vituin-chat.iaas.ull.es/award/' + id + '/json'
                    }
                }
