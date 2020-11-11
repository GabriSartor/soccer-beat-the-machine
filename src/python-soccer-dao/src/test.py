import configparser

from pg_dao import pgDAO

config = configparser.ConfigParser()
config.read('./config.ini')

if "POSTGRESQL" in config:
    print("Instantiating PostgreSQL DAO")
    dao = pgDAO()
    print("Setting psycopg2 connection options")
    dao.config(config)
    print("Creating DB connection and executing tests ...")
    dao.createConnection(connect_timeout = 20)
    dao.testConnection()
    print("Closing connection")
    dao.closeConnection()
else:
    print("There are no postgre options in config.ini")
