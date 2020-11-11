
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
        self.attribute = {primaryKey:id, 'name': name}

    def create(self):
        super.create(self, self.attributes, self.table, self.primaryKey)

    @classmethod
    def fromJson(cls, json):
        data = json.loads(json)
        if not data['id']:
            return None
        id = data['id']
        name = data['name']

        return cls(id, name)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
