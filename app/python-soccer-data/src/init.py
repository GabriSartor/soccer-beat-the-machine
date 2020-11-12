import os
import sys
import json

import click

from exceptions import IncorrectParametersException
from request_handler import RequestHandler

from json_writer import JSonWR

from datetime import date, timedelta

def tree_printer(root):
    for root, dirs, files in os.walk(root):
        for d in dirs:
            print(os.path.join(root, d))   
        for f in files:
            print(os.path.join(root, f))

def main():
    configFile = json.load(open('../config/config.json', 'r'))
    if not configFile:
        click.secho("Could not find configFile", fg="red", bold=True)
        exit(-1)
    
    apikey = configFile['apiToken']
    print("API Token found.")
    print(apikey)
    headers = {'X-Auth-Token': apikey}
    print("Fetching today's date ...")
    
    today = date.today()
    print("Today is: {}".format(today.strftime("%Y-%m-%d")))
    try:
        print("Instatiating request handler")
        #NEED TO MAKE IT A THREAD
        rh = RequestHandler(headers)
        print("Instatiating json Writer and reader")
        js = JSonWR()
        
        for competition in configFile['competitions']:
            print("Trying to fetch information on {}".format(competition['Name']))
            league = rh.get_league(competition['ID'])
            if not league:
                click.secho("League: {} with ID: {} NOT FOUND".format(competition['Name'], competition['ID']), fg="red", bold=True)
                break

            js.save_json(league, ['league', league['id']] )

            season = league['seasons'][0]

            standings = rh.get_standings(league, season = season)
            teams = rh.get_teams_in_league(league, season = season)
            if standings:
                print("Standings fetched for Matchday {}".format(standings['season']['currentMatchday']))
                js.save_json(standings, ['league', 
                                    league['name'], 
                                    'season', 
                                    season['startDate'][:4],
                                    'standings', 
                                    str(standings['season']['currentMatchday'])] )
            else:
                click.secho("NO Standings for this league: {}".format(competition['Name']), fg="red", bold=True)
            
            if teams:
                print("Teams fetched for Season {}".format(standings['season']['startDate']))
                js.save_json(teams, ['league', 
                                    league['name'], 
                                    'season', 
                                    season['startDate'][:4],
                                    'teams'] )
            else:
                click.secho("NO Teams for this league: {}".format(competition['Name']), fg="red", bold=True) 

            matches = rh.get_league_scores(league, season = season)
            if matches:
                print("Matches fetched: {} {}".format(len(matches['matches']), matches['count']))
                js.save_json(matches, ['league', 
                                        league['name'], 
                                        'season', 
                                        season['startDate'][:4],
                                        'matches'] )   
            else:
                click.secho("NO matches for this season", fg="red", bold=True)             
                             
        
    except IncorrectParametersException as e:
        click.secho(str(e), fg="red", bold=True)


if __name__ == '__main__':
    main()
