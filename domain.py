from __future__ import annotations #resolver dependencias circulares
from dataclasses import dataclass, field, asdict
from typing import List
from datetime import datetime
from uuid import UUID
import uuid

def uuid_initializer():
    return uuid.uuid4().hex

@dataclass
class Entity:
    uuid: UUID = field(default_factory = uuid_initializer)
    def to_json(self):
        return asdict(self)

@dataclass
class Issuer(Entity):
    name: str = None
    url: str = None
    badges: list = None

@dataclass
class Person(Entity):
    email: str = None
    awards: List[Award] = None
    slack_id: str = None

@dataclass
class Badge(Entity):
    name: str = None
    description: str = None
    criteria: List[str] = None
    image: str = None

@dataclass
class Badges(Entity):
    badges: List[Badge] = None

@dataclass
class Award(Entity):
    timestamp: datetime = None
    person: Person = None
    badge: Badge = None


@dataclass
class Path:
    '''
    Clase con las rutas donde se aplicará la persistencia de las entidades
    '''
    PERSONS = 'persons.json'
    PERSON = 'person/'
    BADGES = 'badges.json'
    BADGE = 'badge/'
    AWARDS = 'awards.json'
    AWARD = 'award/'
    ISSUER = 'issuer/issuer.json'

@dataclass
class Config:
    '''
    Clase con los elementos de configuracion
    '''
    path: Path


#Probando cosas
if __name__ == '__main__':
    args = {}
    args['name'] = 'medalla de oro'
    args['description'] = 'esto es una medalla de oro'
    args['criteria'] = list()
    args['criteria'].append('tener la puntuacion mas alta')
    args['criteria'].append('ser ganador')
    args['criteria'].append('saber perder')

    badge = Badge(**args)
    json = badge.to_json()
    print(badge)
    print(json)

    badge2 = Badge(**json)
    print("badge2", badge2)
