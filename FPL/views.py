from django.shortcuts import redirect, render
import json
import pandas as pd
import numpy as np



# Create your views here.
def fpl(request):
    import warnings
    warnings.simplefilter(action='ignore')
    gameweek = 1
    #####open json data from file#####
    BASE_DIR = './FPL/'
    fpl_data = open(BASE_DIR+'fpl/'+'response.json')
    data = json.load(fpl_data)
    fixtures_json = open(BASE_DIR+'fpl/'+'fixtures.json')
    GW_fixtures = json.load(fixtures_json)
    ##################################
    elements_df = pd.DataFrame(data['elements'])
    elements_types_df = pd.DataFrame(data['element_types'])
    teams_df = pd.DataFrame(data['teams'])
    gameweeks_df = pd.DataFrame(data['events'])

# 
    GW_df = pd.DataFrame(GW_fixtures)
    GW_df['Home'] = GW_df.team_h.map(teams_df.set_index('id').short_name)
    GW_df['Away'] = GW_df.team_a.map(teams_df.set_index('id').short_name)
    event = GW_df['event'][0]
    GW_df = GW_df.drop(['code','event','finished','finished_provisional','id','minutes','provisional_start_time','started', 'stats', 'team_a', 'team_h'], axis=1) 
# 

    players_df = elements_df[['first_name', 'second_name', 'web_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points', 'event_points']]
    players_df['now_cost'] = players_df['now_cost'].div(10)
    players_df['Position'] = players_df.element_type.map(elements_types_df.set_index('id').singular_name)
    players_df['Value'] = players_df.value_season.astype(float)
    players_df['Team'] = players_df.team.map(teams_df.set_index('id').name)
    players_df = players_df[['web_name','Position', 'Team', 'total_points', 'now_cost', 'Value']]
    players_df.rename(columns={'web_name': 'Name', 'total_points': 'Total points', 'now_cost':'Price'}, inplace=True)
       
    def most_valuable_goalkeepers():
        goal_df = players_df.loc[players_df['Position'] == 'Goalkeeper']
        goal_df = goal_df.drop(['Position'], axis=1)
        most_valuable_goalkeepers = goal_df.sort_values('Value',ascending=False).head(10)
        most_valuable_goalkeepers = most_valuable_goalkeepers.to_html(classes='table table-hover table-borderless', table_id='myTable', justify='left', border=0, index=False)
        return most_valuable_goalkeepers
    def most_valuable_defenders():
        defenders_df = players_df.loc[players_df['Position'] == 'Defender']
        defenders_df = defenders_df.drop(['Position'], axis=1)
        most_valuable_defenders = defenders_df.sort_values('Value',ascending=False).head(10)
        most_valuable_defenders = most_valuable_defenders.to_html(classes='table table-hover table-borderless', table_id='myTable', justify='left', border=0, index=False)
        return most_valuable_defenders
    def most_valuable_midfielders():
        midfielders_df = players_df.loc[players_df['Position'] == 'Midfielder']
        midfielders_df = midfielders_df.drop(['Position'], axis=1)
        most_valuable_midfielders = midfielders_df.sort_values('Value',ascending=False).head(10)
        most_valuable_midfielders = most_valuable_midfielders.to_html(classes='table table-hover table-borderless', table_id='myTable', justify='left', border=0, index=False)
        return most_valuable_midfielders
    def most_valuable_forwards():
        forwards_df = players_df.loc[players_df['Position'] == 'Forward']
        forwards_df = forwards_df.drop(['Position'], axis=1)
        most_valuable_forwards = forwards_df.sort_values('Value',ascending=False).head(10)
        most_valuable_forwards = most_valuable_forwards.to_html(classes='table table-hover table-borderless', table_id='myTable', justify='left', border=0, index=False)
        return most_valuable_forwards
    def most_valuable_teams():
        team_pivot = players_df.pivot_table(index='Team',values='Value',aggfunc=np.mean).reset_index()
        pivot = team_pivot.sort_values('Value',ascending=False).round(2)
        pivot = pivot.to_html(classes='table table-hover table-borderless', table_id='myTable', justify='left', border=0, index=False)
        return pivot

    def players_points():
        import pickle
        # from sklearn.linear_model import Lasso
        # from sklearn.preprocessing import StandardScaler

        loaded_model = pickle.load(open(BASE_DIR+'fpl/'+'Model.pkl', 'rb'))
        predictions = elements_df[['id', 'element_type', 'now_cost', 'team', 'minutes', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'total_points', 'form', 'points_per_game', 'selected_by_percent', 'value_season', 'influence', 'creativity', 'threat', 'ict_index']]
        predictions['form'] = predictions.form.astype('float')
        predictions['points_per_game'] = predictions.points_per_game.astype('float')
        predictions['selected_by_percent'] = predictions.selected_by_percent.astype('float')
        predictions['value_season'] = predictions.value_season.astype('float')
        predictions['influence'] = predictions.influence.astype('float')
        predictions['creativity'] = predictions.creativity.astype('float')
        predictions['threat'] = predictions.threat.astype('float')
        predictions['ict_index'] = predictions.ict_index.astype('float')

        predictions['Predictions'] = loaded_model.predict(predictions)
        predictions['Predictions'] = predictions['Predictions'].astype(int)
        players_points = players_df
        players_points['Predictions'] = predictions['Predictions']
        players_points = players_points.sort_values('Predictions', ascending=False)
        players_points = players_points.to_html(classes='table table-hover table-borderless', table_id='predictions', columns=['Name', 'Position', 'Team', 'Predictions'], justify='left', border=0, index=False)
        return players_points

    def differentials():
        differentials = pd.read_html(players_points())[0]
        differentials = differentials.nlargest(3, 'Predictions', keep='all')
        return differentials

    def fixtures():
        def Home_FDR(row):
            if row['team_h_difficulty'] == 1:
                return 'rgb(55, 85, 35)'
            if row['team_h_difficulty'] == 2:
                return 'rgb(1, 252, 122)'
            if row['team_h_difficulty'] == 3:
                return 'rgb(231, 231, 231)'
            if row['team_h_difficulty'] == 4:
                return 'rgb(255, 23, 81)'
            if row['team_h_difficulty'] == 5:
                return 'rgb(128, 7, 45);'
            
        def Away_FDR(row):
            if row['team_a_difficulty'] == 1:
                return 'rgb(55, 85, 35)'
            if row['team_a_difficulty'] == 2:
                return 'rgb(1, 252, 122)'
            if row['team_a_difficulty'] == 3:
                return 'rgb(231, 231, 231)'
            if row['team_a_difficulty'] == 4:
                return 'rgb(255, 23, 81)'
            if row['team_a_difficulty'] == 5:
                return 'rgb(128, 7, 45);'
        GW_df['Home_FDR'] = GW_df.apply(lambda row: Home_FDR(row), axis=1)
        GW_df['Away_FDR'] = GW_df.apply(lambda row: Away_FDR(row), axis=1)
        return GW_df
    fpl_data.close()
    fixtures_json.close()

    context = {"most_valuable_goalkeepers": most_valuable_goalkeepers(), "most_valuable_defenders": most_valuable_defenders(), "most_valuable_midfielders": most_valuable_midfielders(), "most_valuable_forwards": most_valuable_forwards(), "most_valuable_teams": most_valuable_teams(), "players_points": players_points(), "differentials": differentials(), "fixtures": fixtures(), "event":event}
    return render(request, "fpl.html", context)


def fpl_admin(request):
    import requests
    BASE_DIR = './FPL/'
    response = ""
    if request.method == 'POST':
            week = request.POST.get('gameweek')
            GW_fixtures = requests.get(f"https://fantasy.premierleague.com/api/fixtures?event={week}")
            GW_fixtures = GW_fixtures.json()
            # print(GW_fixtures)
            ######fixtures data######
            with open(BASE_DIR+'fpl/'+'fixtures.json', 'w') as fixtures:
                listed_fixtures = json.dumps(GW_fixtures)
                fixtures.write(listed_fixtures)
            #########################

            #######player data##########
            r = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
            json_data = r.json()
            #####write to text#####
            with open(BASE_DIR+'fpl/'+'response.json', "w") as f:
                listed_data = json.dumps(json_data)
                f.write(listed_data)
            #######################
            response = "successfully generated!!!"
            return render(request, 'fpl_admin_success.html')
    context = {"response": response}
    return render(request, 'fpl_admin.html', context)
