drop view if exists teams_standings ;

create view teams_standings (team_id, season_id, matchday, league_id, points, goals, received_goals, differenza_reti, position)
as 
select team_id, season_id, matchday, league_id, 
		3*((home_w) + (away_w)) + home_t + away_t as points ,  
		home_goals + away_goals as goals, 
		home_received_goals  + away_received_goals as received_goals,  
		home_goals + away_goals - home_received_goals - away_received_goals as differenza_reti,
		RANK () OVER ( PARTITION BY matchday, season_id, league_id
																ORDER BY (3*((home_w) + (away_w)) + home_t + away_t, 
																			home_goals + away_goals - home_received_goals - away_received_goals,
																			home_goals + away_goals) desc, 
																			home_received_goals  + away_received_goals asc
															) rank_number 
from teams_stats ts ;