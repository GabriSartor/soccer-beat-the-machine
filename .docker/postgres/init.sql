DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

GRANT ALL ON SCHEMA public TO "coveto-soccer";

CREATE TYPE match_status AS ENUM ('POSTPONED', 'SCHEDULED', 'SUSPENDED', 'CANCELED', 'LIVE', 'IN_PLAY', 'PAUSED', 'AWARDED', 'FINISHED');
CREATE TYPE match_result AS ENUM ('HOME', 'TIE', 'AWAY');


create table areas (
	area_id INT primary key,
	name varchar
);

create table teams (
	team_id INT primary key,
	area int,
	name varchar ,
	short_name varchar ,
	tla char[3] ,
	venue varchar,
	
	FOREIGN KEY (area) REFERENCES areas(area_id)
);

CREATE TABLE seasons (
	season_id INT primary key,
	start_date date ,
	end_date date ,
	current_matchday smallint ,
	winner int ,
	
	FOREIGN KEY (winner) REFERENCES teams(team_id)
);

CREATE TABLE leagues (
	league_id INT primary key,
	name varchar ,
	code varchar ,
	plan varchar ,
	current_season int,
	area int,
	
	FOREIGN KEY (current_season) REFERENCES seasons(season_id),
	FOREIGN KEY (area) REFERENCES areas(area_id)
);

CREATE TABLE players (
	player_id INT primary key,
	name varchar ,
	first_name varchar ,
	last_name varchar ,
	birth_date date ,
	nationality varchar ,
	position varchar ,
	shirt_number smallint ,
	updated_at timestamp
);

create table matches (
	match_id BIGINT primary key,
	season int,
	utc_date timestamp ,
	matchday smallint ,
	stage varchar ,
	competition_group varchar ,
	home_team int ,
	away_team int ,
	updated_at timestamp ,
	status match_status ,
	winner match_result ,
	home_team_goals smallint ,
	away_team_goals smallint ,
	
	
	FOREIGN KEY (home_team) REFERENCES teams(team_id),
	FOREIGN KEY (home_team) REFERENCES teams(team_id),
	FOREIGN KEY (season) REFERENCES seasons(season_id)
);

create table team_stats (
	league_id int,
	team_id int,
	season_id int,
	position smallint,
    playedGames smallint,
    won smallint,
    draw smallint,
    lost smallint,
    points smallint,
    goalsFor smallint,
    goalsAgainst smallint,
    goalDifference smallint,
	
	primary key (league_id, team_id, season_id),
	FOREIGN KEY (team_id) REFERENCES teams(team_id),
	FOREIGN KEY (league_id) REFERENCES leagues(league_id),
	FOREIGN KEY (season_id) REFERENCES seasons(season_id)
);

create table player_team (
	player_id int,
	team_id int,
	season_id int,
	
	primary key (player_id, team_id, season_id),
	FOREIGN KEY (team_id) REFERENCES teams(team_id),
	FOREIGN KEY (player_id) REFERENCES players(player_id),
	FOREIGN KEY (season_id) REFERENCES seasons(season_id)
);

create table test (
	test_id int primary key,
	test_value varchar
);

insert into test values(1, 'Test');