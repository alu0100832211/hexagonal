from domain import Issuer, Person, Badge, Award, Entity
from dataclasses import fields
import json
import sys, traceback

class Persistence:
    def __init__(self):
        self.path = 'api/'
        pass

    def get_path_list(self, Class: Entity) -> 'List[str]':
        try:
            class_name = Class.__name__.lower()
            with open(self.path + class_name + 's.json') as f:
                class_json = json.load(f)
                return [self.path + class_name + '/' + class_id + '/' + class_name + '.json' for class_id in class_json]
        except:
            traceback.print_exc(file=sys.stdout)

    def load_path_list_entities(self, Class: Entity, path_list) -> 'List[Entity]':
        instances = list()
        try:
            class_fields = fields(Class)
            for path in path_list:
                with open(path) as f:
                    class_json = json.load(f)
                class_params = dict()
                for field in fields(Class):
                    if field in class_json:
                        class_params[field] = class_json[field]
                instances.append(Class(**class_params))
            return instances
        except:
            traceback.print_exc(file=sys.stdout)

    def load_entities(self, Class: Entity):
        try:
            path_list = self.get_path_list(Class)
            return load_path_list_entities(Class, path_list)
        except:
            traceback.print_exc(file=sys.stdout)

    def store_entities(self, Class: Entity, entity_list) -> None:
        try:
           "iterable" in entity_list
        except TypeError:
            entity_list = [entity_list]
        try:
            class_name = Class.__name__.lower()
            entity_list_json = dict()
            for entity in entity_list: # Guardar cada entidad
                entity_list_json[entity.e_id] = class_name
                path_name = self.path + '/' + class_name + '/' \
                        + entity.e_id + '/' + class_name + '.json'
                with open(path_name, 'w') as f:
                    json.dump(asdict(entity), f)
            path_name = self.path + class_name + 's.json' #issuers.json, badges.json, awards.json, persons.json
            with open(path_name, 'w') as f:
                json.dump(entity_list_json, f)
        except:
            traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
    print("Main")
    print (vars(Persistence))
    for var in vars(Persistence):
        print(">>>" + var)
        print(vars(Persistence)[var])

