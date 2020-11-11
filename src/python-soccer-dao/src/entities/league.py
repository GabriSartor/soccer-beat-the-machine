import json

class League(Entity) :
    """
    Entity model for a soccer League
    Attributes:
    #league_id - unique id for a league
    #name - string
    #code - 2 chars
    #plan - string
    #current_season - reference to a season
    #area - reference to an area
    """

    primaryKey = 'league_id'
    table = 'leagues'

    def __init__(self, id, name = None, code = None, plan = None, current_season = None, area = None):
        self.attributes = {primaryKey:id, 'name': name, 'code': code, 'plan': plan, 'current_season': current_season, 'area': area}

    def create(self):
        super.create(self, self.attributes, self.table, self.primaryKey)

    @classmethod
    def fromJson(cls, json):
        data = json.loads(json)
        if not data['id']:
            return None
        id = data['id']
        name = data['name']
        code = data['code']
        plan = data['name']
        current_season = data['currentSeason']['id']
        area = data['area']['id']

        return cls(id, name, code, plan, current_season, area)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self