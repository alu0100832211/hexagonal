from dataclasses import dataclass

@dataclass
class Config:
    '''
    Clase con las rutas donde se aplicará la persistencia de las entidades
    '''
    api_path = 'http://vituin-chat.iaas.ull.es/api'
    PERSONS: str = 'persons.json'
    PERSON: str = 'person/'
    BADGES: str = 'badges.json'
    BADGE: str = 'badge/'
    AWARDS: str = 'awards.json'
    AWARD: str = 'award/'
    ISSUER: str = 'issuer/issuer.json'
