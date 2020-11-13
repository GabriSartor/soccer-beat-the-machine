from datetime import date
from entity import Entity
import json

class Player(Entity):
    """
    Entity model for a soccer player
    Attributes:
    #player_id - unique id for a player
    #name - string
    #first_name - string
    #last_name - string
    #birth_date - date
    #nationality - string
    #position - string
    #updated_at - datetime
    #shirt_number - int
    """
    
    primaryKey = 'player_id'
    table = 'players'

    def __init__(self, id, name = None, first_name = None, last_name = None, 
                birth_date = None, nationality = None, position = None, updated_at = None,
                shirt_number = None):

        self.attributes = {primaryKey:id, 'name' : name, 'first_name' : first_name, 'last_name' : last_name, 
                        'birth_date' : birth_date, 'nationality' : nationality, 'home_team' : position, 'position' : updated_at, 'updated_at' : None,
                        'shirt_number' : shirt_number}

    def create(self):
        super.create(self, self.attributes, self.table, self.primaryKey)

    def update(self):
        super.update(self, self.attributes, self.table, self.primaryKey)

    def get_id(self):
        return self.attributes[self.primaryKey]

    @classmethod
    def fromJson(cls, json):
        data = json.loads(json)
        if not data['id']:
            return None
        id = data['id']
        name = data['name']
        first_name = data['firstName']
        last_name = data['lastName']
        birth_date = data['dateOfBirth']
        nationality = data['nationality']
        position = data['position']
        shirt_number = data['shirtNumber']
        updated_at = data['lastUpdated']

        return cls(id, name, first_name, last_name, 
                birth_date, nationality, position, updated_at,
                shirt_number)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
