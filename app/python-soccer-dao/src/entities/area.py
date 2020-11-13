from entity import Entity
import json

class Area(Entity):
    """
    Entity model for a soccer area
    Attributes:
    #area_id - unique id for an area
    #name - string
    """
    primaryKey = 'area_id'
    table = 'areas'
    
    def __init__(self, id, name = None):
        self.attributes = {self.primaryKey:id, 'name': name}

    def create(self):
        return super().create(self.attributes, self.table, self.primaryKey)

    def update(self):
        return super().update(self.attributes, self.table, self.primaryKey)

    def get_id(self):
        return self.attributes[self.primaryKey]

    @classmethod
    def fromJson(cls, serialized_shit):
        data = json.loads(serialized_shit)
        if not data['id']:
            return None
        id = data['id']
        name = data['name']

        return cls(id, name)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
