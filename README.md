# Soccer: Beat the machine
 A learning project by Gabriele Sartor to make some practice with different technologies and have sum fun with AI-improved soccer stats
 
## Preface
 The project as a whole has the objective to approach some technologies I'm studying both at uni and by myself and to make some experiment with them.
 The main ideas behind the entire architecture is to use small and easily scalable containerized modules with single responisibility and specific personal learning objectives defined a priori.
 Because of this robustness, security and the use of best practices are not always pursued and framework or industry-standard modules are often avoided in favour of more "academic" exercises and challenges.
 
 The only module developed for a more professional environment, and I might say "ready for production", is the web-application which uses the Springboot framework as well as the Tensorflow models served through Tensorflow Serving.

## General architecture
 Every module is containerized and volumes, networks, exposed ports and environment variables are managed by docker-compose. 


## Quick start
 - Create a copy of docker-compose.example.yml, rename it docker-compose.yml and choose a name for the database, user and password
 - Create a copy of app/python-soccer-dao/config/config.example.ini, rename it config.ini and fill it with DB credentials 
 - Create a copy of app/python-soccer-data/config/config.example.json, rename it config.json and insert your API token and the list of competitions and season to be fetched 
 - 

## Soccer Data
 The "Soccer-data" module is a simple Python application that functions as a client for football-data.org APIs.
 Used modules:
 - Click -> for console feedback
 - Requests -> for http requests management
 - ratelimit -> for limiting the number of requests made by minute (since I am using the free version of football-data APIs)

    ### LEARNING OBJECTIVES
    - Manage HTTP requests in a Python application
    - Save results on disk in json format using json python inbuilt methods
    - Use Docker container for a Python application
        - volume mounting and sharing between containers
    - Dockerfile to setup a simple workdir with sources, some data and config files
    - Schedule a job inside a container to automatically update soccer data every day

    ### CONFIGURATION
    There is one configuration file in json format which can be found in app/python-soccer-data/config folder in which must be specified the API authentication Token used to connect to football-data.org and a list of competitions and relative seasons to be fetched from the API. (Competitions IDs can be retrieved with a GET request to football-data.org/v2/competitions/)

    ### INIT
    The init.py script runs when containers are started, it fetches all the data for the list of competitions defined in config.json file and save them in docker shared volume soccer-data, mounted in /usr/app/data

    ### MAIN
    The main.py script runs every day at midnight UTC and fetches all the matches played the day before and updates on the occurring ones. Like init.py script it saves data in json files in soccer-data docker volume.
    If a new season started, teams playing in the league in the new season are fecthed as well.

    ### PROBLEMS TO BE ADDRESSED
    - The rate limit for football-data.org API makes the time needed to fetch data dependent on the number of leagues and seasons. This makes impossible to know when to start running DB queries (see Soccer Dao problems)
    - Files are not yet deleted from the data folder, which makes it not very robust for a long runtime (size will eventually increase)
    - More specific documentation and code comments
    - Lack of input control and exception managament in general (see preface)
    - Lack of unit tests, every change in the code should be made with extreme caution

## Soccer Dao
 The "Soccer-dao" module is a Python application that is in charge of managing data on the DB. It also works as an adapter to insert and extract data from the DB in different formats.
 Used modules:
 - psycopg2 -> for PostgreSQL DB connection and query execution

    ### LEARNING OBJECTIVES
    - Learn to use Python as an Object-Oriented language
        - Entities classes which reflect the DB schema
        - Inheritance
        - Method override
        - ClassMethods to implement the static constructor pattern
    - SQL queries
        - INSERT, UPDATE
        - VIEWS
    - Python dictionaries used as hashmaps to avoid useless queries and duplication problems
    - Design a simple ORM and Migrations system from scratch

    ### DATA MODEL
    Each entity is defined as a Python class which extends the Entity class and provides some methods to build the object from a SELECT query, Json file (from football-data.org API) or CSV file (not yet implemented)
    Example of json files are contained in the model folder

    ### DB MANAGAMENT
    A class named pg_dao has been created to manage every interaction with PostgreSQL Databases: it leverages entities classes to create, update and retrieve data from the DB and this allow for the main scripts not to access or work with the database directly. It has some methods to either execute queries directly or scheduling them to be executed in a subsequent portion of code.

    ### CONFIGURATION
    There is one configuration file in .ini format which can be found in app/python-soccer-dao/config folder in which DB parametres such as host, username, db name and password must be specified. The application is partially set up to be extended to be using other DBMSs as the config.ini sections suggest. (More work to do on this)

    ### INIT
    The init.py script runs when containers are started, it checks for json files in /usr/app/data/init folder and run CREATE queries for Leagues, Season, Teams and Matches and fill relation tables as well.
    Additionally it creates some views to rapidly consult aggregated statistics for each team after each matchday (queries are saved in separate files in queries folder)

    ### MAIN
    The main.py script is a scheduled job and updates all the matches played during the day before and possible updates on the matches yet to be played. Dictionaries are used to compare updates from the API with the actual state of the DB in order to prevent useless queries to be runned. If a new season is present in APIs results and not in DB, the script adds the season and the teams in the DB.
    If at least one match is being updated, so are the statistics views.

    ### DATASET_GENERATOR
    The dataset_generator.py script is a scheduled job that runs two simple queries. Their role is to create a .csv dataset from aggregated statistics which will be used to train and test ML models.

    ### PROBLEMS TO BE ADDRESSED
    - The init procedure is launched by docker-compose when containers are started, this was easy and fast to implement but since the script relies on the data fetched by another service they should be coordinated. Possible solutions:
        - Expose an API from soccer-data to check wheter the fetching is completed, start init process for DB only when a request returns success (microservice architectures should be designed like this)
        - (ACTUAL, BAD PRACTICE) Application sleeps for some seconds before starting its process
    - Exception management is very poor, should be improved considering how many are raised from DB connections and operations
    - More specific documentation and code comments
    - Lack of complete input control (I'm relying way too much on the correctness of soccer-data output) 
    - Lack of unit tests, every change in the code should be made with extreme caution

## Ofelia Scheduler
 The Scheduler model manages scheduled jobs running scripts in other containers. Please refer to https://github.com/mcuadros/ofelia
 Every job is configured in .docker/scheduler/config.ini file, standard Cron syntax is used (seconds included)

 Default configuration includes:
 - FOOTBALL-DATA UPDATE: Every day at 00.00am UTC python-soccer-data/main.py script is run
 - DB-DATA UPDATE: Every day at 1.00am UTC python-soccer-dao/main.py script is run 
 - TRAINING-DATASET UPDATE: On the first day of every month the training_dataset for ml models are updated

## Database
 The database used is a PostgreSQL instance, dockerized as well as the other services.
 Configuration is inside the docker-compose file, data are persisted when containers are down thanks to the postgres-data volume.
 An init file is mounted in the default postgres directory and it will be run only if postgres-data volume is empty.
 Referential integrity is implemented for each table, indexing is still missing and performance have not yet been measured and optimized.