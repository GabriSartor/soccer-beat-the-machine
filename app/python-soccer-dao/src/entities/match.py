from datetime import datetime
from entity import Entity
import json

class Match(Entity):
    """
    Entity model for a soccer match
    Attributes:
    #match_id - unique id for a match
    #season - reference to a season
    #utc_date - datetime
    #matchday - int
    #stage - string
    #competition_group - string
    #home_team - reference to a team
    #away_team - reference to a team
    #updated_at - datetime
    #match_status - enum MatchStatus
    #home_team_goals - int 
	#away_team_goals - int 
    """

    primaryKey = 'match_id'
    table = 'matches'

    def __init__(self, id, season = None, utc_date = None, matchday = None, 
                stage = None, competition_group = None, home_team = None, away_team = None, updated_at = None,
                match_status = None, home_team_goals = None, away_team_goals = None, winner = None):

        self.attributes = {self.primaryKey:id, 'season' : season, 'utc_date' : utc_date, 'matchday' : matchday, 
                        'stage' : stage, 'competition_group' : competition_group, 'home_team' : home_team, 'away_team' : away_team, 'updated_at' : None,
                        'status' : match_status, 'home_team_goals' : home_team_goals, 'away_team_goals' : away_team_goals , 'winner': winner}

    def create(self):
        self.attributes['updated_at'] = datetime.utcnow().strftime('%Y-%m-%d, %H:%M:%S');
        return super().create(self.attributes, self.table, self.primaryKey)

    def update(self):
        self.attributes['updated_at'] = datetime.utcnow().strftime('%Y-%m-%d, %H:%M:%S');
        return super().update(self.attributes, self.table, self.primaryKey)

    def get_id(self):
        return self.attributes[self.primaryKey]

    @classmethod
    def fromJson(cls, serializeds):
        data = json.loads(serializeds)
        if not data['id']:
            return None
        id = data['id']
        season = data['season']['id']
        utc_date = data['utcDate']
        matchday = data['matchday']
        stage = data['stage']
        competition_group = data['group']
        home_team = data['homeTeam']['id']
        away_team = data['awayTeam']['id']
        updated_at = data['lastUpdated']
        match_status = data['status']
        home_team_goals = data['score']['fullTime']['homeTeam']
        away_team_goals = data['score']['fullTime']['awayTeam']
        if home_team_goals is not None and away_team_goals is not None:
            if (home_team_goals > away_team_goals):
                winner = 'HOME' 
            elif (home_team_goals < away_team_goals):
                winner = 'AWAY'
            else:
                winner = 'TIE'
        else:
            winner = None

        return cls(id, season, utc_date, matchday, 
                stage, competition_group, home_team, away_team, updated_at,
                match_status, home_team_goals, away_team_goals, winner)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
        
    @classmethod
    def fromDB(cls, attributes):
        return cls(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5],
        attributes[6], attributes[7], attributes[8], attributes[9], attributes[10], attributes[11],
        attributes[12])
