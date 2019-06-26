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
    e_id: UUID = field(default_factory = uuid_initializer)
    name: str = None
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
    description: str = None
    criteria: List[str] = None
    image: str = None

@dataclass
class Award(Entity):
    timestamp: datetime = None
    person: Person = None
    badge: Badge = None

#Probando cosas
if __name__ == '__main__':
    pass
