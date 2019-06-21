#encoding utf-8

from domain import Issuer, Person, Badge, Award
from typing import List
from datetime import datetime
import json, os
from config import Config

class Application:
    def __init__(self, config = None):
        self.config = config
        try:
            with open(badges_path()) as f:
                badge_ids = json.load(f)
                self.badges = list()
                for badge_id in badge_ids:
                    with open(badge_path(badge_id=badge_id)) as f:
                        self.badges.append(Badge(json.load(f)))
#            with open(self.config.PERSONS, 'r') as f:
#                self.persons = json.load(f)["persons"]
#                for person_id in self.persons:
#                    filename = self.config.person + person_id + '.json'
#                    self.person = dict()
#                    with open(filename, 'r') as f:
#                        self.person[person_id] = json.load(f)
#            with open(self.config.AWARDS, 'r') as f:
#                self.awards = json.load(f)["awards"]
#                for award_id in self.awards:
#                    filename = self.config.award + award_id + '.json'
#                    self.award = dict()
#                    with open(filename, 'r') as f:
#                        self.award[award_id] = json.load(f)
#            with open(self.config.issuer, 'r') as f:
#                self.issuer = json.load(f)["issuer"]
#
        except Exception as error:
            sys.exit(str(error))

    def badges_path(self):
        return str(self.config.BADGES)

    def badge_path(self, badge: Badge = None, badge_id: str = None):
        if badge:
            badge_id = badge.badge_id
        return str(self.config.BADGE + badge_id + '.json')

    def create_badge(self, **params):
        new_badge = Badge(params)
        for badge in self.badges:
            if badge.name == new_badge.name:
                return

        self.badges.append(new_badge)
        with open(badge_path(new_badge), 'w') as f:
            json.dump(new_badge.to_json())

    def assign(self, badge: Badge, person: Person):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        new_award = Award(badge=badge, person=person, timestamp=timestamp)
        person.awards.append(new_award)

    def owns(self, person: Person, badge: Badge):
        for award in person.awards:
            if award.badge == badge:
                return True
        return False


    def rm_badge(self, badge: Badge):
        path = 'badge/' + badge.uid
        os.remove(path)

if __name__ = '__main__':
    config = Config()
    app = Application(config())
