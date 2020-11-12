from datetime import datetime

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
                match_status = None, home_team_goals = None, away_team_goals = None):

        self.attributes = {primaryKey:id, 'season' : season, 'utc_date' : utc_date, 'matchday' : matchday, 
                        'stage' : stage, 'competition_group' : competition_group, 'home_team' : home_team, 'away_team' : away_team, 'updated_at' : None,
                        'match_status' : match_status, 'home_team_goals' : home_team_goals, 'away_team_goals' : away_team_goals}

    def create(self):
        super.create(self, self.attributes, self.table, self.primaryKey)

    @classmethod
    def fromJson(cls, json):
        data = json.loads(json)
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

        return cls(id, season, utc_date, matchday, 
                stage, competition_group, home_team, away_team, updated_at,
                match_status, home_team_goals, away_team_goals)
    
    @classmethod
    def fromCsv(cls, data):
        ##Create object from data
        return self
