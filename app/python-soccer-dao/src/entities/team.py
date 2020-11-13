from datetime import date
from entity import Entity
import json

class Team(Entity):
    """
    Entity model for a soccer sTeameason
    Attributes:
    #team_id - unique id for a Team
    #area - reference to an area
    #name - string
    #short_name - string
    #tla - char 3
    #venue - string
    #updated_at - datetime
    """

    primaryKey = 'team_id'
    table = 'teams'

    def __init__(self, id, area = None, name = None, short_name = None, 
                tla = None, venue = None, updated_at = None):

        self.attributes = {self.primaryKey :id, 'area' : area, 'name' : name, 'short_name' : short_name, 
                        'tla' : tla, 'venue' : venue, 'updated_at' : updated_at}

    def create(self):
        return super().create(self.attributes, self.table, self.primaryKey)

    def update(self):
        return super().update(self.attributes, self.table, self.primaryKey)

    def get_id(self):
        return self.attributes[self.primaryKey]

    @classmethod
    def fromJson(cls, serialized):
        data = json.loads(serialized)
        if not data['id']:
            return None
        id = data['id']
        area = data['area']['id']
        name = data['name']
        short_name = data['shortName']
        tla = data['tla']
        venue = data['venue']
        updated_at = data['lastUpdated']

        return cls(id, area, name, short_name, 
                tla, venue, updated_at)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
