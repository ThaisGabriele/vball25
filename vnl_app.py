import streamlit as st
import pandas as pd

# interactive plots
import plotly.graph_objs as go
import plotly.express as px

st.set_page_config("🏐"
    'VNL 2025',
    layout="wide"
)

header = st.container()
general_stats, teams_details, stats_by_position = st.tabs(['General stats', 'Teams details',  'Stats by Position'])
# get_df_sets() - get from standings the amount of sets won and lost by each team, with these two values we calculate the amount of sets played  
def get_df_sets(df_scorers):
    
    standings = pd.read_html("https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/standings/women/#advanced")
    
    df1 = standings[0]['Unnamed: 1_level_0']
    
    df1.rename(columns= {'Unnamed: 1_level_1':'Team'}, inplace=True)
    
    df2 = standings[0]['Sets']
    
    del df2['Set Ratio']
    
    res = pd.concat([df1, df2], axis=1)
    
    res.replace({'Team': {'USAUSA':'United StatesUSA'}}, inplace=True)

    res['Team'] = res['Team'].apply(lambda row : row[0:-3])

    res = res.assign(Sets = lambda n : n['Won'] + n['Lost'])

    res = res.filter(['Team','Won', 'Lost','Sets'])
    
    df = pd.merge(df_scorers, res, on="Team")
      
    return df

def get_skills_per_sets(teams):
    
    attack_per_set = lambda x : round((teams['Pts. de ataque'] / teams['Sets']),1)
    block_per_set = lambda x : round((teams['Pts. de bloqueio'] / teams['Sets']),1)
    serve_per_set = lambda x : round((teams['Pts. de saque'] / teams['Sets']),1)
    rec_per_set = lambda x : round((teams['Successful'] / teams['Sets']),1)
    dig_per_set = lambda x : round((teams['Digs'] / teams['Sets']),1)
    
    teams['AttackPerSet'] = attack_per_set('AttackPerSet')
    teams['BlockPerSet'] = block_per_set('BlockPerSet')
    teams['ServePerSet'] = serve_per_set('ServePerSet')
    teams['ExcRecPerSet'] = rec_per_set('ExcRecPerSet')
    teams['DigPerSet'] = dig_per_set('DigPerSet')
    
    return teams
 
def interactive_plot_attack(teams):
    
    teams = teams.sort_values("AttackPerSet", ascending=False).head(10)
    
    st.markdown(""" **General Stats** """)
    #st.dataframe(teams.set_index('Team'))
    trace1 = go.Bar(
                y = teams.AttackPerSet,
                x = teams.Team,
                name = "Attack",
                marker = dict(color = 'rgba(255, 174, 255, 0.9)',
                             line=dict(color='rgb(0,0,0)',width=1.9)),
                text = teams.AttackPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Pts. de ataques/Sets')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    

def interactive_plot_block(teams):
    
    teams = teams.sort_values("BlockPerSet", ascending=False).head(10)
    
    trace1 = go.Bar(
                    y = teams.BlockPerSet,
                    x = teams.Team,
                    name = "Block",
                    marker = dict(color = 'rgba(255, 255, 128, 0.9)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.BlockPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Bloqueios/Sets')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    
def interactive_plot_serve(teams):
    
    teams = teams.sort_values("ServePerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.ServePerSet,
                    x = teams.Team,
                    name = "Serve",
                    marker = dict(color = 'rgba(170, 255, 128, 0.9)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.ServePerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Aces/Sets')

    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    
def interactive_plot_digs(teams):
    
    teams = teams.sort_values("DigPerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.DigPerSet,
                    x = teams.Team,
                    name = "Digs",
                    marker = dict(color = 'rgba(114, 189, 246, 0.8)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.DigPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Defesas/Sets')

    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)


def interactive_plot_receptions(teams):
    
    teams = teams.sort_values("ExcRecPerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.ExcRecPerSet,
                    x = teams.Team,
                    name = "Excellent Reception",
                    marker = dict(color = 'rgba(246, 1, 73, 0.75)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.ExcRecPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Recepções perfeitas/Sets')

    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)


def load_scorers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-scorers/"
    
    best_scorers = pd.read_html(url)[0]
    
    best_scorers = best_scorers.rename(columns={
                'Rankrank': 'Rank',
                'Player NamePlayer':'Player', 
                'TeamTeam':'Team',
                'PointsPts':'Pts. Totais',
                'Attack PointsA Pts':'Pts. de ataque', 
                'Block PointsB Pts':'Pts. de bloqueio', 
                'Serve PointsS Pts':'Pts. de saque'

    })
      
    return best_scorers

def get_attackers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-attackers/"
    
    best_attackers = pd.read_html(url)[0]
    
    best_attackers = best_attackers.rename(columns={
        'Rankrank': 'Rank',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
        'Pointsattacks':'AttackPoints',
        'ErrorsSE':'Errors', 
        'Attemptsshots':'AttemptsShots',
        'Average per matchaverage-per-match':'AveragePerMatch', 
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_attackers[(best_attackers['TotalAttempts'] > 0)]

    return df

def get_receivers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-receivers/"
    
    best_receivers = pd.read_html(url)[0]
    
    best_receivers = best_receivers.rename(columns={
        'Rankrank': 'Rank',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
         'SuccesfulSuccesful':'Successful',
        'ErrorsSE':'Errors', 
        'AttempsAtt':'Attempts',
        'Average per matchaverage-per-match':'AveragePerMatch',
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_receivers[(best_receivers['TotalAttempts'] > 0)]
    
    return df
    
def get_diggers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-diggers/"
    
    best_diggers = pd.read_html(url)[0]
    
    best_diggers = best_diggers.rename(columns={
        'Rankrank': 'Rank',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
        'SuccessfulSuccessful':'Successful',
        'Digsgreat-save':'Digs',
        'ErrorsSE':'Errors', 
        'ReceptionsRec':'Receptions',
        'Average per matchaverage-per-match':'AveragePerMatch',
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_diggers[(best_diggers['Digs'] > 0)]
    
    return df

    
def get_blockers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-blockers/"
    
    best_blockers = pd.read_html(url)[0]
    
    best_blockers = best_blockers.rename(columns={
         'Rankrank':'Rank', 
         'Player NamePlayer':'Player', 
         'TeamTeam':'Team',
         'Blocksstuff-blocks':'Blocks', 
         'ErrorsSE': 'Errors', 
         'ReboundsREB':'Rebounds',
         'Average per matchaverage-per-match': 'AveragePerMatch', 
         'Efficiency %Eff':'Efficiency%', 
         'TotalTA':'TotalAttempts'
    })
    df = best_blockers[(best_blockers['TotalAttempts'] > 0)]
    
    return df

def get_servers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-servers/"
    
    best_servers = pd.read_html(url)[0]
    
    best_servers = best_servers.rename(columns={
        'Rankrank': 'Rank',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
        'Pointsserve-points': 'ServePoints',
        'ErrorsSE':'Errors', 
        'AttempsAtt':'Attempts',
        'Average per matchaverage-per-match':'AveragePerMatch', 
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    df = best_servers[(best_servers['ServePoints'] > 0)]
      
    return df

def players_by_team(df_scorers, sigla):  
    
    players = df_scorers[df_scorers['Team'] == sigla]
  
    del players['RankRank']
        
    st.markdown(""" **Team Stats** """)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pts. Totais", players['Pts. Totais'].sum())
    col2.metric("Pts. de ataque", players['Pts. de ataque'].sum())
    col3.metric("Pts. de bloqueio", players['Pts. de bloqueio'].sum())
    col4.metric("Pts. de saque", players['Pts. de saque'].sum())

    st.markdown(""" **Players Stats** """)
    del players['Team']
    col1, col2 = st.columns(2)
    with col1:
         st.dataframe(players.set_index('Player'))
    with col2:
         gen_bar_chart_scorers(players)

def show_skill_tables(code):
    
    st.markdown(""" **Attacking** """)
    df_attack = get_attackers()
    df_attack = df_attack[df_attack['Team'] == code]
    del df_attack['Team']
    st.data_editor(df_attack.set_index('Player'))
    
    st.markdown(""" **Reception** """)
    df_rec = get_receivers()
    st.dataframe(df_rec[df_rec['Team'] == code].set_index('Player'))
    
    st.markdown(""" **Diggers** """)
    df_dig = get_diggers()
    st.dataframe(df_dig[df_dig['Team'] == code].set_index('Player'))
        
    st.markdown(""" **Blocking** """)
    df_blk =  get_blockers()
    st.dataframe(df_blk[df_blk['Team'] == code].set_index('Player'))
    
    st.markdown(""" **Serving** """)
    df_serve = get_servers()
    st.dataframe(df_serve[df_serve['Team'] == code].set_index('Player'))



def gen_bar_chart_scorers(df):
    
    min_points = 0
    df = df[df['Pts. Totais'] > min_points].sort_values('Pts. Totais', ascending=True)
    fig = px.bar(df, title = 'Brasil - Maiores pontuadoras', x = 'Pts. Totais', y = 'Player', text ='Pts. Totais', color = 'Pts. Totais', color_continuous_scale = px.colors.sequential.Viridis, height=450, width=500)
    fig.update_layout(xaxis_title="", yaxis_title="", font = dict(family = 'Sans Serif', size = 12), showlegend=True)
    fig.update_yaxes(showgrid=False)
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig)


#### Starts here!

with header:
    st.title("Welcome to my VNL 2025 app!")
    st.text("Another way to check the numbers from the competition - team by team")
    st.text("by Thaís G. (@BRA_VolleyStats)")
    st.markdown("""
    *All data collected from the [official website of the competition](https://br.volleyballworld.com/volleyball/competitions/volleyball-nations-league/statistics/women/best-scorers/)* 
    """)
    
    st.info(""" [PT] Todos os dados são retirados do site da volleyball world. 
    São fornecidos por eles e do jeito deles. As estatísticas fornecidas podem ser interpretadas como:
    * Pts. Totais: total de pontos feitos por uma jogadora
    * Pts. de ataque : pontos de ataque
    * Pts. de bloqueio:  pontos de bloqueios
    * Pts. de saque: pontos de saque ou 'aces'
    * Digs: defesas perfeitas  
    * Successful ou  Excellent Reception: refere-se a apenas recepções excelentes feitas por uma jogadora
    * Success% : é equivalente a percentual de ataque ou aproveitamento de ataque, é dado pelo total de pontos de ataque feitos pelo total de tentativas de ataque
    * AttackPerSet: é dado pelo total de pontos de ataque feitos pelo time pelo total de sets jogados pelo time. 
    **usa-se a mesma lógica para os outros fundamentos*
    """)
    
with general_stats:

    df_scorers = load_scorers()
    
    df_scorers = df_scorers.filter(items=['Team', 'Pts. de ataque','Pts. de bloqueio', 'Pts. de saque', 'Pts. Totais']).groupby("Team").sum()

    df_scorers = df_scorers.reset_index()
    
    df_digs = get_diggers()
    df_digs = df_digs.groupby("Team").sum().reset_index()
    
    df_rec = get_receivers()
    df_rec = df_rec.groupby("Team").sum().reset_index()
    
    df_scorers = pd.merge(df_scorers, df_digs[['Team','Digs']], on=['Team'])
    
    df_scorers = pd.merge(df_scorers, df_rec[['Team','Successful']], on=['Team'])
    
    df_scorers['Team'] = df_scorers['Team'].replace({
                                            'THA':'Thailand',
                                            'BUL':'Bulgaria',
                                            'TUR':'Türkiye',
                                            'ITA':'Italy',
                                            'BRA':'Brazil',
                                            'GER':'Germany',
                                            'DOM':'Dominican Republic',
                                            'USA':'United States',
                                            'NED':'Netherlands',
                                            'CHN':'China',
                                            'FRA':'France',
                                            'SRB':'Serbia',
                                            'CAN':'Canada',
                                            'POL':'Poland',
                                            'JPN':'Japan',
                                            'KOR':'Korea'
    })
    
    
    df_scorers = get_df_sets(df_scorers)
     
    new_df = get_skills_per_sets(df_scorers)
    
    st.dataframe(new_df.set_index('Team'))
    
    df_attack_metrics= get_attackers()
    
    df_attack_metrics = df_attack_metrics.filter(items=['Team','AttackPoints','Errors','TotalAttempts']).groupby(['Team']).sum().reset_index()
    
    df_attack_metrics = (df_attack_metrics.assign(AtaquePerc = lambda x : round((df_attack_metrics['AttackPoints']/df_attack_metrics['TotalAttempts'])*100,1) ))
    
    df_attack_metrics = (df_attack_metrics.assign(AtaqueEf = lambda x : round(((df_attack_metrics['AttackPoints'] - df_attack_metrics['Errors']) /df_attack_metrics['TotalAttempts'])*100,1) ))

    st.markdown(""" **Attack %** """)
    st.dataframe(df_attack_metrics.set_index('Team'))
    
    df_rec_metrics= get_receivers()
    
    df_rec_metrics = df_rec_metrics.filter(items=['Team','Successful','Errors','TotalAttempts']).groupby(['Team']).sum().reset_index()
    
    df_rec_metrics = (df_rec_metrics.assign(RecPerfPerc = lambda x : round((df_rec_metrics['Successful']/df_rec_metrics['TotalAttempts'])*100,1) ))

    st.markdown(""" **Excellent reception %** """)
    st.dataframe(df_rec_metrics.set_index('Team'))

    df_dig_metrics= get_diggers()
    
    df_dig_metrics = df_dig_metrics.filter(items=    ['Team','Digs','Errors','TotalAttempts']).groupby(['Team']).sum().reset_index()
    
    df_dig_metrics = (df_dig_metrics.assign(DigsPerc = lambda x : round((df_dig_metrics['Digs']/df_dig_metrics['TotalAttempts'])*100,1)))
    st.markdown(""" **Perfect digs %** """)   
    st.dataframe(df_dig_metrics.set_index('Team'))
    
    df_serve_metrics= get_servers()
    
    df_serve_metrics = df_serve_metrics.filter(items=    ['Team','ServePoints','Errors','TotalAttempts']).groupby(['Team']).sum().reset_index()
    
    df_serve_metrics = (df_serve_metrics.assign(AcesPerc = lambda x : round((df_serve_metrics['ServePoints']/df_serve_metrics['TotalAttempts'])*100,1)))
    
    st.markdown(""" **Service %** """)    
    st.dataframe(df_serve_metrics.set_index('Team'))
    
    interactive_plot_attack(new_df)

    interactive_plot_block(new_df)

    interactive_plot_serve(new_df)   
    
    interactive_plot_receptions(new_df) 
    
    interactive_plot_digs(new_df)   
    
with teams_details:
    
    st.title("Choose a team: ")
    
    team = st.selectbox(
     '',
         ('Brasil','Bulgária','Canadá','China',
           'República Dominicana','França','Alemanha','Itália', 
          'Japão','Coreia', 'Holanda','Polônia', 
          'Sérvia','Tailândia', 'Turquia','Estados Unidos','Repúplica Tcheca','França'
         ))

    st.markdown(f"""## {team}""")
    df_scorers = load_scorers()

    if team == 'Brasil':
        code = 'BRA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Bulgária':
        code = 'BUL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'França':
        code = 'FRA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Canadá':
        code = 'CAN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)    

    elif team == 'China':
        code = 'CHN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'República Dominicana':
        code = 'DOM' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)

    elif team == 'Alemanha':
        code = 'GER' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Itália':
        code = 'ITA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
   
    elif team == 'Japão':
        code = 'JPN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Coreia':
        code = 'KOR' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)    

        
    elif team == 'Holanda':
        code = 'NED' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Polônia':
        code = 'POL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
                         
    
    elif team == 'Sérvia':
        code = 'SRB' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Tailândia':
        code = 'THA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
                         

    elif team == 'Turquia':
        code = 'TUR' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
              
    elif team == 'Estados Unidos':
        code = 'USA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    elif team == 'República Tcheca':
        code = 'CZE' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'França':
        code = 'FRA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)

with stats_by_position:
		
    st.title("Choose a position: ")
    st.info("""    
		* Posições:
    	* MB : central
    	* OH: ponteira
    	* O: oposto
    	* L: líbero """
    )
    df_players = pd.read_csv('vnl25_players.csv', index_col=False)
    del df_players['No.']
    df_scorers = load_scorers()
    position = st.selectbox("Choose a position: ", ["MB","OH","O","L"])
    df_players = df_players.query("Position == @position")
    
    cols = ['Player','Team','Pts. Totais','Pts. de ataque', 'Pts. de bloqueio', 'Pts. de saque']
    df = pd.merge(df_players, df_scorers, on=['Player','Team'])
    df = df.filter(items=cols).set_index('Player')
    
    
    if (position == "OH") or (position == "MB") or (position == "O"):
       st.markdown(""" **Scorers** """)
       st.dataframe(df)
       st.markdown(""" **Attack** """)
       df_att = get_attackers()
       df1 = pd.merge(df_players, df_att, on=['Player','Team'])
       st.dataframe(df1.set_index('Player'))
       df_blk = get_blockers()
       st.markdown(""" **Block**""")
       df2 = pd.merge(df_players, df_blk, on=['Player','Team'])
       st.dataframe(df2.set_index('Player'))
       if (position == "OH"):
    	   df_rec = get_receivers()
    	   st.markdown(""" **Reception**""")
    	   df = pd.merge(df_players, df_rec, on=['Player','Team'])
    	   st.dataframe(df.set_index('Player'))           
   
    elif position == 'L':
    	df_rec = get_receivers()
    	st.markdown(""" **Reception**""")
    	df = pd.merge(df_players, df_rec, on=['Player','Team'])
    	st.dataframe(df.set_index('Player'))
    	df_dig = get_diggers()
    	st.markdown(""" **Defense**""")
    	df = pd.merge(df_players, df_dig, on=['Player','Team'])
    	st.dataframe(df.set_index('Player'))
  
    
    
