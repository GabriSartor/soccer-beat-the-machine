from datetime import date
class Season(Entity):
    """
    Entity model for a soccer season
    Attributes:
    #season_id - unique id for a season
    #start_date - date
    #end_date - date
    #curent_matchday - integer
    #winner - reference to Team entity
    """

    primaryKey = 'season_id'
    table = 'seasons'

    def __init__(self, id, name = None, start_date = None, end_date = None, 
                currentMatchday = None, winner = None):

        self.attributes = {primaryKey:id, 'name' : name, 'start_date' : start_date, 'end_date' : end_date, 
                        'curent_matchday' : curent_matchday, 'winner' : winner}

    def create(self):
        super.create(self, self.attributes, self.table, self.primaryKey)

    @classmethod
    def fromJson(cls, json):
        data = json.loads(json)
        if not data['id']:
            return None
        id = data['id']
        name = data['name']
        start_date = data['startDate']
        end_date = data['endDate']
        curent_matchday = data['currentMatchday']
        winner = data['winner']

        return cls(id, name, start_date, end_date, 
                curent_matchday, winner)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
