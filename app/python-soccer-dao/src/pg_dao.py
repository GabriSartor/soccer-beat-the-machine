import configparser
import sys
import psycopg2
sys.path.append('entities/')

from league import League
from area import Area
from match import Match
from player import Player
from season import Season
from team import Team

class pgDAO:
    def __init__(self):
        self.async_queries = ''

    def config(self, config):
        self.dbname = config['POSTGRESQL']['dbname']
        self.dbuser = config['POSTGRESQL']['dbuser']
        self.dbpassword = config['POSTGRESQL']['dbpassword']
        self.dbhost = config['POSTGRESQL']['dbhost']
        self.dbport = config['POSTGRESQL']['dbport']
    
    def createConnection(self, connect_timeout = 5):
        self.connection = psycopg2.connect( dbname=self.dbname, 
                                            user=self.dbuser,
                                            password=self.dbpassword,
                                            host=self.dbhost,
                                            port=self.dbport,
                                            connect_timeout = connect_timeout )

    def testConnection(self):
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT * FROM test;")
        print(self.cur.fetchone())

    def closeConnection(self):
        if self.connection:
            self.connection.close()

    def executeQuery(self, query):
        if not self.connection:
            return False
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        cur.close()
        return True

    def executeAsync(self):
        if not self.connection:
            return False
        cur = self.connection.cursor()
        if self.async_queries:
            try:
                cur.execute(self.async_queries)
                self.connection.commit()
            except:
                print("Errore nella query:")
                print(self.async_queries.replace(";", ";\n"))
            cur.close()
            self.async_queries = ''
            return True
        return False

    def scheduleAsyncQuery(self, query):
        self.async_queries += query
        
    def clearAsyncQuery(self, query):
        self.async_queries = ''

    def statsViewGenerate(self, string):
        try:
            self.executeQuery(string)
        except:
            print("Errore nella creazione della view di statistiche")

    def getAllAreas(self):
        query = "SELECT * FROM areas;"
        if not self.connection:
            return False
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        result = []
        for record in cur.fetchall():
            a = Area.fromDB(record)
            result.append(a)
        cur.close()
        return result
    
    def getAllTeams(self):
        query = "SELECT * FROM teams;"
        if not self.connection:
            return False
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        result = []
        for record in cur.fetchall():
            a = Area.fromDB(record)
            result.append(a)
        cur.close()
        return result
    
    def getAllLeagues(self):
        query = "SELECT * FROM leagues;"
        if not self.connection:
            return False
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        result = []
        for record in cur.fetchall():
            l = League.fromDB(record)
            result.append(l)
        cur.close()
        return result
    
    def getAllMatches(self, season_id):
        query = "SELECT * FROM matches WHERE season = {}".format(season_id)
        if not self.connection:
            return False
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        result = []
        for record in cur.fetchall():
            m = Match.fromDB(record)
            result.append(m)
        cur.close()
        return result
    
    def getAllSeasons(self):
        query = "SELECT * FROM seasons"
        if not self.connection:
            return False
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        result = []
        for record in cur.fetchall():
            s = Season.fromDB(record)
            result.append(s)
        cur.close()
        return result

    def getHomeTrainingSet(self):
        with open('queries/home_training_set.sql', 'r') as sql_file:
            query = sql_file.read()
            if not self.connection:
                return None
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()
            result =  cur.fetchall()
            cur.close()
            return result
        return None
    
    def getAwayTrainingSet(self):
        with open('queries/away_training_set.sql', 'r') as sql_file:
            query = sql_file.read()
            if not self.connection:
                return None
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()
            result =  cur.fetchall()
            cur.close()
            return result
        return None

    def saveHomeTrainingSetAsCSV(self, fileName):
        if not self.connection:
            return False
        
        with open('../queries/home_training_set.sql', 'r') as sql_file:
            query = sql_file.read()
            cur = self.connection.cursor()

            outputquery = 'copy ({0}) to stdout with csv header'.format(query)

            with open(fileName, 'w') as f:
                cur.copy_expert(outputquery, f)
                
            cur.close()
            return True

    def saveAwayTrainingSetAsCSV(self, fileName):
        if not self.connection:
            return False
        
        with open('../queries/away_training_set.sql', 'r') as sql_file:
            query = sql_file.read()
            cur = self.connection.cursor()

            outputquery = 'copy ({0}) to stdout with csv header'.format(query)

            with open(fileName, 'w') as f:
                cur.copy_expert(outputquery, f)
                
            cur.close()
            return True
