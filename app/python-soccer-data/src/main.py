import os
import sys
import json

import click

from exceptions import IncorrectParametersException
from request_handler import RequestHandler

from json_writer import JSonWR

from datetime import date, timedelta


def main():
    configFile = json.load(open('config/config.json', 'r'))
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
        rh = RequestHandler(headers)
        print("Instatiating json Writer and reader")
        js = JSonWR()
        
        for competition in configFile['competitions']:
            print("Trying to fetch information on {}".format(competition['Name']))
            league = rh.get_league(competition['ID'])
            if not league:
                click.secho("League: {} with ID: {} NOT FOUND".format(competition['Name'], competition['ID']), fg="red", bold=True)
                break

            js.save_json(league, ['league', league['name']] )

            
            #if first_install:
            #    for season in seasons:
            #        teams = rh.get_teams_in_league(league, season)
            #        standings = rh.get_standings(league, season)
            #        matches = rh.get_league_scores(league, season)
            #        js.save_json(teams, ['league', league['name'], 'season', season['startDate'][:4],'teams'] )
            #        js.save_json(standings, ['league', league['name'], 'season', season['startDate'][:4],'standings'])
            #        js.save_json(matches, ['league', league['name'], 'season', season['startDate'][:4],'matches'])   
            #else:
            season = league['seasons'][0]

            standings = rh.get_standings(league, season = season)
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

            new_matches = rh.get_league_scores(league, dateFrom = today, dateTo = (today + timedelta(days=7)))
            if new_matches:
                print("New Matches fetched for the next week: {}".format(len(new_matches['matches'])))
                js.save_json(new_matches, ['league', 
                                        league['name'], 
                                        'season', 
                                        season['startDate'][:4],
                                        'new_matches',
                                        today.strftime("%d_%m")] )   
            else:
                click.secho("NO new matches for this week", fg="red", bold=True)         

            played_matches = rh.get_league_scores(league, dateFrom = (today - timedelta(days=1)), dateTo = (today - timedelta(days=1)))
            if played_matches:
                print("Matches played yesterday: {}".format(len(played_matches['matches'])))
                js.save_json(played_matches, ['league', 
                                        league['name'], 
                                        'season', 
                                        season['startDate'][:4],
                                        'played_matches'],
                                        today.strftime("%d_%m") )   
            else:
                click.secho("NO matches played yesterday", fg="red", bold=True)         
                             
        
    except IncorrectParametersException as e:
        click.secho(str(e), fg="red", bold=True)


if __name__ == '__main__':
    main()
