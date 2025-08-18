from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import teams

all_teams = teams.get_teams()
player_dictionary = [player for player in players.get_players() if player["is_active"]]

all_teams = teams.get_teams()

def get_shot_data_team(team_nickname, year):
    team_info = [team for team in all_teams if team['nickname'] == team_nickname][0]
    team_id = team_info['id']

    team_shotlog = shotchartdetail.ShotChartDetail(
        team_id=team_id, player_id=0,
        context_measure_simple='FGA',
        season_nullable=f"{year}-{year-2000+1}",
        season_type_all_star=['Regular Season']
    ).get_data_frames()[0]

    return team_shotlog

def get_shot_data_player(player_full_name):
    player_info = [player for player in player_dictionary if player['full_name'] == player_full_name][0]
    player_id = player_info['id']
    print(player_id)

    player_shotlog = shotchartdetail.ShotChartDetail(
        team_id=0, player_id=player_id,
        context_measure_simple='FGA',
        season_nullable="2024-25",
        season_type_all_star=['Regular Season', 'Playoffs']
    )

    player_df = player_shotlog.get_data_frames()[0]
    return player_df