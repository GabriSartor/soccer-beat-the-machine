import configparser
import os

from pg_dao import pgDAO

def initPGConn(config):
    print("Instantiating PostgreSQL DAO")
    dao = pgDAO()
    print("Setting psycopg2 connection options")
    dao.config(config)
    print("Creating DB connection ...")
    dao.createConnection(connect_timeout = 20)

def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    dao = None
    if "POSTGRESQL" in config:
        dao = initPGConn(config)
    with os.scandir('my_directory/') as entries:
        for entry in entries:
            print(entry.name)

        
    if not dao:
        return        
    else:
        print("There are no postgre options in config.ini")

main()


#for competition list
            #load competition and seasons
            #save area
            #for season list
                #load teams and standings
                #save teams
                #save standings
                #for teams list
                    #load players
            #for each team_id
                #load all teams