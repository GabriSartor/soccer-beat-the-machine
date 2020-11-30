import configparser
import os
import time
import sys
import json

from datetime import date, timedelta

sys.path.append('entities/')

from pg_dao import pgDAO

from league import League
from area import Area
from match import Match
from player import Player
from season import Season
from team import Team

def initPGConn(config):
    print("Instantiating PostgreSQL DAO")
    dao = pgDAO()
    print("Setting psycopg2 connection options")
    dao.config(config)
    print("Creating DB connection ...")
    dao.createConnection(connect_timeout = 50)
    return dao

def main():
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
    
    competitions_list = set()
    with os.scandir('../data/updates') as entries:
        for entry in entries:
            s = entry.name.replace('.json', '').split('_')
            if 'league' in s and not s[1] in competitions_list:
                competitions_list.add(s[1])
    if not competitions_list:
        return

    today = date.today()

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

    ##Riempio le mappe dal DB

    for league_id in competitions_list:

        #Apro il file della lega
        with open('../data/updates/league_{}.json'.format(league_id), 'r') as file:
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

            dao.executeAsync()

            stats_query = ''
            #Ciclo per ogni stagione (per ora solo la prima)
            for s in deserialized_data['seasons'][:1]:
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
                dao.executeAsync()

                matches_map = {}
                for match in dao.getAllMatches(season.get_id()):
                    if not matches_map.get(match.get_id()):
                        matches_map[match.get_id()] = match

                if new_season:
                   #Per ogni stagione guardo le squadre
                    with open('../data/updates/league_{}_season_{}_updated_teams.json'.format(league_id, season.attributes['start_date'][:4]), 'r') as team_file:
                        print("Opened json file for Teams in season {}".format(season.attributes['start_date'][:4]))
                        team_data = team_file.read()
                        team_deserialized_data = json.loads(team_data)
                        print("Found {} teams".format(len(team_deserialized_data['teams'])))
                        new_teams_counter = 0; old_teams_counter = 0; no_teams_counter = 0
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
                            elif teams_map.get(team.get_id()) != team:
                                dao.scheduleAsyncQuery(team.update())
                                old_teams_counter += 1
                            else:
                                no_teams_counter += 1
                            if new_season:
                                stats_query += 'INSERT INTO team_league (league_id, team_id, season_id) VALUES ({}, {}, {});'.format(league.get_id(), team.get_id(), season.get_id())

                        print("Found {} new teams, {} updated teams and {} old teams".format(new_teams_counter, old_teams_counter, no_teams_counter))
                        dao.executeAsync()                
                
                #E i match
                #league_ID_season_YEAR_updated_matches_DATE  
                with open('../data/updates/league_{}_season_{}_updated_matches_{}.json'.format(league_id, season.attributes['start_date'][:4], today.strftime("%Y_%m_%d")), 'r') as match_file:
                    print("Opened json file for Matches in season {}".format(season.attributes['start_date'][:4]))
                    match_data = match_file.read()
                    match_deserialized_data = json.loads(match_data)
                    print("Found {} matches".format(len(match_deserialized_data['matches'])))
                    new_matches_counter = 0; old_matches_counter = 0; no_matches_counter = 0
                    for m in match_deserialized_data['matches']:
                        match = Match.fromJson(json.dumps(m))
                        if not match.get_id() in matches_map:
                            matches_map[match.get_id()] = match
                            dao.scheduleAsyncQuery(match.create())
                            new_matches_counter += 1
                        elif matches_map.get(match.get_id()) != match:
                            dao.scheduleAsyncQuery(match.update())
                            old_matches_counter += 1
                        else:
                            no_matches_counter += 1

                    print("Found {} new matches, {} updated matches and {} old matches ".format(new_matches_counter, old_matches_counter, no_matches_counter))
                    dao.executeAsync()

            if not league.get_id() in leagues_map:
                leagues_map[league.get_id()] = league
                dao.scheduleAsyncQuery(league.create())
            elif leagues_map.get(league.get_id) != league:
                dao.scheduleAsyncQuery(league.update())

            print("League found and created-> ID: {} name: {}".format(league.attributes['league_id'], league.attributes['name']))
            print("Executing queries...")
            if dao.executeAsync():
                print("Succeded!")
                if new_season:
                    print("Executing stats queries...")
                    if dao.executeQuery(stats_query):
                        print("Succeded!")
                    else:
                        print("There's been an error in updating the database")
            else:
                print("There's been an error in updating the database")

    dao.executeQuery('REFRESH MATERIALIZED VIEW teams_stats;')
    dao.executeQuery('REFRESH MATERIALIZED VIEW teams_standings;')
    print("Views updated")

            

if __name__ == '__main__':
    main()
