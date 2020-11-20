drop  view if exists teams_stats CASCADE ;

create view teams_stats (team_id, league_id, matchday, season_id, home_goals, away_goals, home_received_goals, away_received_goals, home_w, home_t, home_l, away_w, away_t, away_l)
as 
	select t.team_id , l.league_id , m.matchday , m.season , 
															coalesce((select sum(m2.home_team_goals)
															from matches m2
															where m2.home_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday ) , 0)
															, coalesce((select sum(m2.away_team_goals)
															from matches m2
															where m2.away_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday ), 0)
															, coalesce((select sum(m2.home_team_goals)
															from matches m2
															where m2.away_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday ), 0)
															, coalesce((select sum(m2.away_team_goals)
															from matches m2
															where m2.home_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday ), 0)
															, (
															select count(*)
															from matches m2
															where m2.home_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday and m2.winner = 'HOME')
															, (
															select count(*)
															from matches m2
															where m2.home_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday and m2.winner = 'TIE')
															, (
															select count(*)
															from matches m2
															where m2.home_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday and m2.winner = 'AWAY')
															, (
															select count(*)
															from matches m2
															where m2.away_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday and m2.winner = 'AWAY')
															, (
															select count(*)
															from matches m2
															where m2.away_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday and m2.winner = 'TIE')
															, (
															select count(*)
															from matches m2
															where m2.away_team = t.team_id and m2.season = m.season and m2.matchday <= m.matchday and m2.winner = 'HOME')
	from teams t , leagues l , matches m, team_league tl , seasons s 
	where t.team_id = tl.team_id and l.league_id = tl.league_id and m.season = tl.season_id and s.season_id = m.season 
			and (m.home_team = t.team_id or m.away_team = t.team_id)
			and m.matchday <= s.current_matchday 
			
	group by t.team_id , l.league_id , m.matchday , m.season ;