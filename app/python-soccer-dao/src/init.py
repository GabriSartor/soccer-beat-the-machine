import configparser
import os
import time
import sys
import json

sys.path.append('entities/')

from pg_dao import pgDAO

from league import League
from area import Area
from match import Match
from player import Player
from season import Season
from team import Team

def tree_printer(root):
    for root, dirs, files in os.walk(root):
        for d in dirs:
            print(os.path.join(root, d))   
        for f in files:
            print(os.path.join(root, f))

def initPGConn(config):
    print("Instantiating PostgreSQL DAO")
    dao = pgDAO()
    print("Setting psycopg2 connection options")
    dao.config(config)
    print("Creating DB connection ...")
    dao.createConnection(connect_timeout = 50)
    return dao

def main():
    time.sleep(10)
    config = configparser.ConfigParser()
    config.read('../config/soccer_dao_config.ini')
    dao = None
    if "POSTGRESQL" in config:
        dao = initPGConn(config)    
        if not dao:
            print("No connection could be established")
            return        
        else:
            print("Connected...")
    else:
        print("There are no postgre options in config.ini")
        return

    print("Finding new files to upload ...")
    competitions_list = set()
    with os.scandir('../data/init') as entries:
        for entry in entries:
            s = entry.name.replace('.json', '').split('_')
            if 'league' in s and not s[1] in competitions_list:
                competitions_list.add(s[1])
    if not competitions_list:
        return

    areas_map = {}
    leagues_map = {}
    teams_map = {}

    for league_id in competitions_list:
        seasons_map = {}
        #Apro il file della lega
        with open('../data/init/league_{}.json'.format(league_id), 'r') as file:
            data = file.read()
            deserialized_data = json.loads(data)
            league = League.fromJson(data)
            area = Area.fromJson(json.dumps(deserialized_data['area']))
            if not area.get_id() in areas_map:
                areas_map[area.get_id()] = area
                dao.scheduleAsyncQuery(area.create())

            stats_query = ''
            #Ciclo per ogni stagione (per ora solo la prima)
            for s in deserialized_data['seasons'][:1]:
                season = Season.fromJson(json.dumps(s))
                #Aggiorno la lista delle stagioni
                if not season.get_id() in seasons_map:
                    seasons_map[season.get_id()] = season
                    dao.scheduleAsyncQuery(season.create())

                #Per ogni stagione guardo le squadre
                with open('../data/init/league_{}_season_{}_teams.json'.format(league_id, season.attributes['start_date'][:4]), 'r') as team_file:
                    team_data = team_file.read()
                    team_deserialized_data = json.loads(team_data)
                    for t in team_deserialized_data['teams']:
                        team = Team.fromJson(json.dumps(t))
                        if not team.get_id() in teams_map:
                            teams_map[team.get_id()] = team
                            dao.scheduleAsyncQuery(team.create())
                        else:
                            dao.scheduleAsyncQuery(team.update())

                        stats_query += 'INSERT INTO team_league (league_id, team_id, season_id) VALUES ({}, {}, {});'.format(league.get_id(), team.get_id(), season.get_id())

                #E i match
                with open('../data/init/league_{}_season_{}_matches.json'.format(league_id, season.attributes['start_date'][:4]), 'r') as match_file:
                    match_data = match_file.read()
                    match_deserialized_data = json.loads(match_data)
                    for m in match_deserialized_data['matches']:
                        match = Match.fromJson(json.dumps(m))
                        dao.scheduleAsyncQuery(match.create())

            if not league.get_id() in leagues_map:
                leagues_map[league.get_id()] = league
                dao.scheduleAsyncQuery(league.create())

            print("League found and created-> ID: {} name: {}".format(league.attributes['league_id'], league.attributes['name']))
            print("Executing queries...")
            if dao.executeAsync():
                print("Succeded!")
            else:
                print("mmmmmmmm")
            print("Executing stats queries...")
            if dao.executeQuery(stats_query):
                print("Succeded!")
            else:
                print("mmmmmmmm")

    with open('team_stats_view.sql', 'r') as sql_file:
        dao.executeQuery(sql_file.read())
            

main()