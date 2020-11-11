import os
import sys
import json

import click

from exceptions import IncorrectParametersException
from request_handler import RequestHandler

from json_writer import JSonWR

from datetime import date, timedelta

def load_json(file):
    """Load JSON file at app start"""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, file)) as jfile:
        data = json.load(jfile)
    return data


def get_input_key():
    """Input API key and validate"""
    click.secho("No API key found!", fg="yellow", bold=True)
    click.secho("Please visit {} and get an API token.".format(RequestHandler.BASE_URL),
                fg="yellow",
                bold=True)
    while True:
        confkey = click.prompt(click.style("Enter API key",
                                           fg="yellow", bold=True))
        if len(confkey) == 32:  # 32 chars
            try:
                int(confkey, 16)  # hexadecimal
            except ValueError:
                click.secho("Invalid API key", fg="red", bold=True)
            else:
                break
        else:
            click.secho("Invalid API key", fg="red", bold=True)
    return confkey


def load_config_key():
    """Load API key from config file, write if needed"""
    global api_token
    try:
        api_token = os.environ['SOCCER_CLI_API_TOKEN']
    except KeyError:
        config = ("./.soccer-cli.ini")
        with open(config, "r") as cfile:
            key = cfile.read()
        if key:
            api_token = key
        else:
            os.remove(config)  # remove 0-byte file
            click.secho('No API Token detected. '
                        'Please visit {0} and get an API Token, '
                        'which will be used by Soccer CLI '
                        'to get access to the data.'
                        .format(RequestHandler.BASE_URL), fg="red", bold=True)
            sys.exit(1)
    return api_token


def main():
    configFile = json.load(open('config/config.json', 'r'))
    if not configFile:
        click.secho("Could not find configFile", fg="red", bold=True)
        exit(-1)
    print("API Token found.")
    
    apikey = configFile['apiToken']
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
