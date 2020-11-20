import requests
import click
from exceptions import APIErrorException
from datetime import date
from ratelimit import limits, sleep_and_retry

class RequestHandler(object):

    PERIOD = 65
    CALLS = 10
    BASE_URL = 'http://api.football-data.org/v2/'
    LIVE_URL = 'http://soccer-cli.appspot.com/'

    def __init__(self, headers):
        self.headers = headers
        self.req_count = 0

    @sleep_and_retry
    @limits(calls=CALLS, period=PERIOD)
    def _get(self, url, params = None):
        """Handles api.football-data.org requests"""
        req = requests.get(RequestHandler.BASE_URL + url, headers=self.headers, params=params)
        print(req.url)
        status_code = req.status_code
        if status_code == requests.codes.ok:
            return req
        elif status_code == requests.codes.bad:
            raise APIErrorException('Invalid request. Check parameters.')
        elif status_code == requests.codes.forbidden:
            raise APIErrorException('This resource is restricted')
        elif status_code == requests.codes.not_found:
            raise APIErrorException('This resource does not exist. Check parameters')
        elif status_code == requests.codes.too_many_requests:
            raise APIErrorException('You have exceeded your allowed requests per minute/day')

    def get_league(self, league):
        """Queries the API and gets the list of seasons available for the league"""
        try:
            req = self._get('competitions/{league_id}'.format(
                        league_id=league))
            league_details = req.json()
            if len(league_details["seasons"]) == 0:
                return
            else:
                return league_details
        except APIErrorException as e:
            click.secho(e.args[0],
                        fg="red", bold=True)

    def get_teams_in_league(self, league, season = None):
        """Queries the API and gets the list of teams participating in specified league"""
        try:
            params = {}
            if season:
                params['season'] = season['startDate'][:4]

            http_query = 'competitions/{league_id}/teams'.format(league_id=league['id'])
            req = self._get(http_query, params)
            league_teams = req.json()
            if len(league_teams["teams"]) == 0:
                return
            else:
                return league_teams
        except APIErrorException as e:
            click.secho(e.args[0],
                        fg="red", bold=True)

    def get_standings(self, league, season = None):
        """
        Queries the API and fetches the scores for fixtures
        based upon the league and time parameter
        """  
        try:
            params = {}
            if season:
                params['season'] = season['startDate'][:4]

            http_query = 'competitions/{id}/standings'.format(id=league['id'])
            req = self._get(http_query, params)
            league_standings = req.json()
            if len(league_standings["standings"]) == 0:
                return
            else:
                return league_standings
        except APIErrorException as e:
            click.secho(e.args[0],
                            fg="red", bold=True)

    def get_league_scores(self, league, season = None, onlyFinished = False, dateFrom = None, dateTo = None, matchFilter = None):
        """
        Queries the API and fetches the scores for fixtures
        based upon the league and time parameter
        """  
        try:
            params = {}
            if season:
                params['season'] = season['startDate'][:4]
            if dateFrom:
                params['dateFrom'] = dateFrom.strftime("%Y-%m-%d")
            if dateTo:
                params['dateTo'] = dateTo.strftime("%Y-%m-%d")
            if onlyFinished:
                params['status'] = 'FINISHED'
            if matchFilter:
                params['stage'] = matchFilter
            http_query = 'competitions/{id}/matches'.format(id=league['id'])
            req = self._get(http_query, params)
            fixtures_results = req.json()
            # no fixtures in the past week. display a help message and return
            if len(fixtures_results["matches"]) == 0:
                return
            return fixtures_results
        except APIErrorException as e:
            click.secho(e.args[0],
                        fg="red", bold=True)

    def get_team_players(self, team):
        """
        Queries the API and fetches the players
        for a particular team
        """
        try:
            req = self._get('teams/{}/'.format(team['id']))
            team_players = req.json()['squad']
            if not team_players:
                return
            else:
                return team_players
        except APIErrorException as e:
            click.secho(e.args[0],
                        fg="red", bold=True)

    def get_team_scores(self, team, season):
        """Queries the API and gets the particular team scores"""
        try:
            req = self._get('teams/{team_id}/matches?season={season_year}'.format(
                        team_id=team['id'], season_year=season['startDate'][:4]))
            team_scores = req.json()
            if len(team_scores["matches"]) == 0:
                return
            else:
                return team_scores
        except APIErrorException as e:
            click.secho(e.args[0],
                        fg="red", bold=True)

    def reset_req_count(self):
        self.req_count = 0