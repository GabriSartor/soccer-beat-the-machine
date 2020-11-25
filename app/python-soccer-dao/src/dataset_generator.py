import configparser
import os
import time
import sys
import json

from datetime import date, timedelta

from pg_dao import pgDAO

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
    #config.read('../config/soccer_dao_config.ini')
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

    ret = dao.saveHomeTrainingSetAsCSV('../data/dataset/home_training_set.csv')
    ret2 = dao.saveAwayTrainingSetAsCSV('../data/dataset/away_training_set.csv')
    if ret and ret2:
        print("DONE!")
    else:
        print("Oh no :(")

main()