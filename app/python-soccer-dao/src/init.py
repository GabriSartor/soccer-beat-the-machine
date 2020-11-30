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
    #Wait for the data fetcher to ask resources from Football API
    #And for the DB to be up and ready
    time.sleep(20)
    #time.sleep(15)
    config = configparser.ConfigParser()
    config.read('../config/config.ini')
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
    competitions_list = {}
    with os.scandir('../data/init') as entries:
        for entry in entries:
            #league_{ID}_season_{YEAR}_...
            s = entry.name.replace('.json', '').split('_')
            if 'league' in s and not s[1] in competitions_list:
                competitions_list[s[1]] = set()
            if 'season' in s and s[3] not in competitions_list[s[1]]:
                competitions_list[s[1]].add(s[3])

    if not competitions_list:
        return

    areas_map = {}
    leagues_map = {}
    teams_map = {}

    areas_map = {}
    for area in dao.getAllAreas():
        if not areas_map.get(area.get_id()):
            areas_map[area.get_id()] = area

    leagues_map = {}
    for league in dao.getAllLeagues():
        if not leagues_map.get(league.get_id()):
            leagues_map[league.get_id()] = league

    teams_map = {}
    for team in dao.getAllTeams():
        if not teams_map.get(team.get_id()):
            teams_map[team.get_id()] = team
    print("Found {} leagues:".format(len(competitions_list)))
    for key, value in competitions_list.items():
        print("League {} with {} seasons".format(key, value))

    for league_id in competitions_list.keys():
        
        #Apro il file della lega
        with open('../data/init/league_{}.json'.format(league_id), 'r') as file:
            print("Opened json file for League {}".format(league_id))
            data = file.read()
            deserialized_data = json.loads(data)
            league = League.fromJson(data)
            print("League object created, ID: {} name: {}".format(league.get_id(), league.attributes['name']))
            area = Area.fromJson(json.dumps(deserialized_data['area']))
            print("Area object created, ID: {} name: {}".format(area.get_id(), area.attributes['name']))
            if not area.get_id() in areas_map:
                areas_map[area.get_id()] = area
                dao.scheduleAsyncQuery(area.create())
                print("Area does not exist, running CREATE query")
            elif areas_map.get(area.get_id) != area:
                dao.scheduleAsyncQuery(area.update())
                print("Area does exist, running UPDATE query")

            seasons_map = {}
            for season in dao.getAllSeasons():
                if not seasons_map.get(season.get_id()):
                    seasons_map[season.get_id()] = season
                    
            stats_query = ''
            #Ciclo per ogni stagione (per ora solo la prima)
            for s in deserialized_data['seasons'][:len(competitions_list[league_id])]:
                new_season = False
                season = Season.fromJson(json.dumps(s))
                print("Season object created, startDate: {}".format(season.attributes['start_date']))
                #Aggiorno la lista delle stagioni
                if not season.get_id() in seasons_map:
                    #### NB #########
                    #Iniziata una nuova stagione, devi salvare le SQUADRE
                    new_season = True
                    seasons_map[season.get_id()] = season
                    dao.scheduleAsyncQuery(season.create())
                    print("Season does not exist, running CREATE query")
                elif seasons_map.get(season.get_id) != season:
                    dao.scheduleAsyncQuery(season.update())
                    print("Season does exist, running UPDATE query")

                matches_map = {}
                for match in dao.getAllMatches(season.get_id()):
                    if not matches_map.get(match.get_id()):
                        matches_map[match.get_id()] = match

                #Per ogni stagione guardo le squadre
                with open('../data/init/league_{}_season_{}_teams.json'.format(league_id, season.attributes['start_date'][:4]), 'r') as team_file:
                    print("Opened json file for Teams in season {}".format(season.attributes['start_date'][:4]))
                    team_data = team_file.read()
                    team_deserialized_data = json.loads(team_data)
                    print("Found {} teams".format(len(team_deserialized_data['teams'])))
                    new_teams_counter = 0; old_teams_counter = 0
                    for t in team_deserialized_data['teams']:   
                        team = Team.fromJson(json.dumps(t))
                        if not t['area']['id'] in areas_map:
                            print("Team {} name {} is in a different Area from League".format(team.get_id(), team.attributes['name']))
                            area = Area.fromJson(json.dumps(t['area']))
                            print("Area object created, ID: {} name: {}".format(area.get_id(), area.attributes['name']))
                            areas_map[area.get_id()] = area
                            dao.scheduleAsyncQuery(area.create())

                        if not team.get_id() in teams_map:
                            teams_map[team.get_id()] = team
                            dao.scheduleAsyncQuery(team.create())
                            new_teams_counter += 1
                        else:
                            dao.scheduleAsyncQuery(team.update())
                            old_teams_counter += 1
                        if new_season:
                            stats_query += 'INSERT INTO team_league (league_id, team_id, season_id) VALUES ({}, {}, {});'.format(league.get_id(), team.get_id(), season.get_id())

                    print("Found {} new teams and {} old teams".format(new_teams_counter, old_teams_counter))

                #E i match
                with open('../data/init/league_{}_season_{}_matches.json'.format(league_id, season.attributes['start_date'][:4]), 'r') as match_file:
                    print("Opened json file for Matches in season {}".format(season.attributes['start_date'][:4]))
                    match_data = match_file.read()
                    match_deserialized_data = json.loads(match_data)
                    print("Found {} matches".format(len(match_deserialized_data['matches'])))
                    new_matches_counter = 0; old_matches_counter = 0
                    for m in match_deserialized_data['matches']:
                        match = Match.fromJson(json.dumps(m))
                        if not match.get_id() in matches_map:
                            matches_map[match.get_id()] = match
                            dao.scheduleAsyncQuery(match.create())
                        elif matches_map.get(match.get_id()) != match:
                            dao.scheduleAsyncQuery(match.update())

                    print("Found {} new matches and {} old matches".format(new_matches_counter, old_matches_counter))

            if not league.get_id() in leagues_map:
                leagues_map[league.get_id()] = league
                dao.scheduleAsyncQuery(league.create())
            elif leagues_map.get(league.get_id()) != league:
                dao.scheduleAsyncQuery(league.update())

            print("League found and created-> ID: {} name: {}".format(league.attributes['league_id'], league.attributes['name']))
            print("Now executing queries...")
            if dao.executeAsync():
                print("Succeded!")
            else:
                print("There's been an error in updating the database")
            if new_season:
                print("Executing stats queries...")
                if dao.executeQuery(stats_query):
                    print("Succeded!")
                else:
                    print("There's been an error in updating the database")

    with open('../queries/team_stats_view.sql', 'r') as sql_file:
        dao.executeQuery(sql_file.read())

    with open('../queries/team_standings_view.sql', 'r') as sql_file:
        dao.executeQuery(sql_file.read())

if __name__ == '__main__':
    main()
