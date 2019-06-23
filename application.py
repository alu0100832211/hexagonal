#encoding utf-8

from domain import Issuer, Person, Badge, Award
from typing import List
from datetime import datetime
import json, os, sys
from config import Config

class Application:
    def __init__(self, config = None):
        self.config = config

    def list_badges(self):
        """Devuelve diccionario con nombre del badge
        y su correspondiente png
        """
        with open("api/badges.json") as f:
            return json.load(f)

# Esto va en persistence.py
    def badges_path(self):
        return str(self.config.BADGES)

    def badge_path(self, badge: Badge = None, badge_id: str = None):
        if badge:
            badge_id = badge.badge_id
        return str(self.config.BADGE + badge_id + '.json')

    def create_badge(self, **params):
        badge_params = ["name", "description", "criteria", "image"]
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

if __name__ == '__main__':
    config = Config()
    app = Application(config())
