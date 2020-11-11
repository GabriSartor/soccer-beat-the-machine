import configparser

from pg_dao import pgDAO

config = configparser.ConfigParser()
config.read('./config.ini')

if "POSTGRESQL" in config:
    print("Instantiating PostgreSQL DAO")
    dao = pgDAO()
    print("Setting psycopg2 connection options")
    dao.config(config)
    print("Creating DB connection ...")
    dao.createConnection(connect_timeout = 20)

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

    dao.testConnection()
    print("Closing connection")
    dao.closeConnection()
else:
    print("There are no postgre options in config.ini")
