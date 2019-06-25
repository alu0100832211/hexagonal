#encoding utf-8

from domain import Issuer, Person, Badge, Award
from typing import List
from datetime import datetime
import json, os, sys
from config import Config
from persistence import Persistence

class Application:
    def __init__(self, p: Persistence):
        self.badges = p.load_entities(Badge)
        self.persons = p.load_entities(Person)
        self.issuers = p.load_entities(Issuer)
        self.awards = p.load_entities(Award)

    def list_badges(self):
        """Devuelve diccionario con nombre del badge
        y su correspondiente png
        """
        with open("api/badges.json") as f:
            return json.load(f)

# Esto va en persistence.py
    def has_badge(self, badge_id):
        for badge in self.badges:
            if badge.id == badge_id:
                return True
        return False

    def badges_path(self):
        return str(self.config.BADGES)

    def badge_path(self, badge: Badge = None, badge_id: str = None):
        if badge:
            badge_id = badge.badge_id
        return str(self.config.BADGE + badge_id + '.json')

    def create_badge(self, name, description, criteria, image):
        new_badge = Badge()
        new_badge.name = name
        new_badge.description = description
        new_badge.criteria = criteria
        new_badge.image = image

        for badge in self.badges:
            if badge.name == new_badge.name:
                return None

        self.badges.append(new_badge)
        p.store_entites
        return new_badge
        #self.persistence.badge(new_badge)

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

def entities(entities):
    if not iter(entity):
        entities = list(entities)
    for entity in entities:
        print(entity)
if __name__ == '__main__':
    a = 1
    entitites(a)

