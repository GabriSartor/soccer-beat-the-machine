import os
import sys
import json

import click

from exceptions import IncorrectParametersException
from request_handler import RequestHandler

from json_writer import JSonWR

from datetime import date, timedelta, datetime

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
        js = JSonWR('../data/updates')
        
        for competition in configFile['competitions']:
            print("Trying to fetch information on {}".format(competition['Name']))
            league = rh.get_league(competition['ID'])
            if not league:
                click.secho("League: {} with ID: {} NOT FOUND".format(competition['Name'], competition['ID']), fg="red", bold=True)
                break

            season = league['seasons'][0]
            new_season = False
            last_season_updated = js.open_json(['league', 
                                        str(league['id'])])['seasons'][0]
            if season != last_season_updated:
                new_season = True
            
            update_matches = rh.get_league_scores(league, matchFilter = competition['matchFilter'], dateFrom = (today - timedelta(days=1)), dateTo= datetime.strptime(season['endDate'], '%Y-%m-%d'))

            if new_season:
                update_teams = rh.get_teams_in_league(league, season = season)
                if update_teams:
                    print("New Season update available, teams fetched: ".format(len(update_teams['teams'])))
                    js.save_json(update_teams, ['league', 
                                        str(league['id']), 
                                        'season', 
                                        season['startDate'][:4],
                                        'updated_teams'])
            if update_matches:
                print("New Matches fetched: {}".format(len(update_matches['matches'])))
                js.save_json(update_matches, ['league', 
                                        str(league['id']), 
                                        'season', 
                                        season['startDate'][:4],
                                        'updated_matches',
                                        today.strftime("%Y_%m_%d")] )
                js.save_json(league, ['league', 
                                        str(league['id'])])
            else:
                click.secho("NO new matches for this week", fg="red", bold=True)              

    except IncorrectParametersException as e:
        click.secho(str(e), fg="red", bold=True)

if __name__ == '__main__':
    main()
