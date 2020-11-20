from datetime import date
from entity import Entity
import json

class Season(Entity):
    """
    Entity model for a soccer season
    Attributes:
    #season_id - unique id for a season
    #start_date - date
    #end_date - date
    #curent_matchday - integer
    """

    primaryKey = 'season_id'
    table = 'seasons'

    def __init__(self, id, start_date = None, end_date = None, 
                currentMatchday = None, winner = None):

        self.attributes = {self.primaryKey:id, 'start_date' : start_date, 'end_date' : end_date, 
                        'current_matchday' : currentMatchday}

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
        start_date = data['startDate']
        end_date = data['endDate']
        curent_matchday = data['currentMatchday']

        return cls(id, start_date, end_date, 
                curent_matchday)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self

    @classmethod
    def fromDB(cls, attributes):
        return cls(attributes[0], attributes[1], attributes[2], attributes[3])
