class Award:
    def __init__ (self, id, email, timestamp, badge_url):
        self.id = id
        self.email = email
        self.timestamp = timestamp
        self.badge_url = badge_url

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
                    "url": 'http://vituin-chat.iaas.ull.es/api/award/' + id + '/json'
                    }
                }
