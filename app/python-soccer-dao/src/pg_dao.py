import configparser

import psycopg2


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
            cur.execute(self.async_queries)
            self.connection.commit()
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
