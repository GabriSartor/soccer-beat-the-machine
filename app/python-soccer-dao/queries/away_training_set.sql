select ts1.team_id as team_1_id, ts1.home_goals as team_1_home_goals, ts1.away_goals as team_1_away_goals, 
ts1.home_received_goals as team_1_home_received_goals, ts1.away_received_goals as team_1_away_received_goals, 
ts1.home_w as team_1_home_w, ts1.home_t as team_1_home_t, ts1.home_l as team_1_home_l, ts1.away_w as team_1_away_w, 
ts1.away_t as team_1_away_t, ts1.away_l as team_1_away_l,
ts2.team_id as team_2_id, ts2.home_goals as team_2_home_goals, ts2.away_goals as team_2_away_goals, 
ts2.home_received_goals as team_2_home_received_goals, ts2.away_received_goals as team_2_away_received_goals, 
ts2.home_w as team_2_home_w, ts2.home_t as team_2_home_t, ts2.home_l as team_2_home_l, ts2.away_w as team_2_away_w, 
ts2.away_t as team_2_away_t, ts2.away_l as team_2_away_l,
m.season as match_season, m.matchday as matchday ,
m.winner as winner, m.home_team_goals as match_home_goals, m.away_team_goals as match_away_goals
from teams_stats ts1 , teams_stats ts2 , matches m
where m.away_team = ts1.team_id and m.season = ts1.season_id and m.matchday = ts1.matchday - 1 
	and m.home_team = ts2.team_id and m.season = ts2.season_id and m.matchday = ts2.matchday -1