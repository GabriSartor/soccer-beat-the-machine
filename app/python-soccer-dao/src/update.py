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
            data = file.read()
            deserialized_data = json.loads(data)
            league = League.fromJson(data)
            area = Area.fromJson(json.dumps(deserialized_data['area']))
            if not area.get_id() in areas_map:
                areas_map[area.get_id()] = area
                dao.scheduleAsyncQuery(area.create())
            elif areas_map.get(area.get_id) != area:
                dao.scheduleAsyncQuery(area.update())

            seasons_map = {}
            for season in dao.getAllSeasons():
                if not seasons_map.get(season.get_id()):
                    seasons_map[season.get_id()] = season

            stats_query = ''
            #Ciclo per ogni stagione (per ora solo la prima)
            for s in deserialized_data['seasons'][:1]:
                new_season = False
                season = Season.fromJson(json.dumps(s))
                #Aggiorno la lista delle stagioni
                if not season.get_id() in seasons_map:
                    #### NB #########
                    #Iniziata una nuova stagione, devi salvare le SQUADRE ( o rilanciare init.py )
                    new_season = True
                    seasons_map[season.get_id()] = season
                    dao.scheduleAsyncQuery(season.create())
                elif seasons_map.get(season.get_id) != season:
                    dao.scheduleAsyncQuery(season.update())

                matches_map = {}
                for match in dao.getAllMatches(season.get_id()):
                    if not matches_map.get(match.get_id()):
                        matches_map[match.get_id()] = match

                if new_season:
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
                #league_ID_season_YEAR_updated_matches_DATE  
                with open('../data/updates/league_{}_season_{}_updated_matches_{}.json'.format(league_id, season.attributes['start_date'][:4], today.strftime("%Y_%m_%d")), 'r') as match_file:
                    match_data = match_file.read()
                    match_deserialized_data = json.loads(match_data)
                    for m in match_deserialized_data['matches']:
                        match = Match.fromJson(json.dumps(m))
                        if not match.get_id() in matches_map:
                            matches_map[match.get_id()] = match
                            dao.scheduleAsyncQuery(match.create())
                        elif matches_map.get(match.get_id) != match:
                            dao.scheduleAsyncQuery(match.update())

            if not league.get_id() in leagues_map:
                leagues_map[league.get_id()] = league
                dao.scheduleAsyncQuery(league.create())
            elif leagues_map.get(league.get_id) != league:
                dao.scheduleAsyncQuery(league.update())

            print("League found and created-> ID: {} name: {}".format(league.attributes['league_id'], league.attributes['name']))
            print("Executing queries...")
            if dao.executeAsync():
                print("Succeded!")
            else:
                print("mmmmmmmm")

if __name__ == '__main__':
    main()
