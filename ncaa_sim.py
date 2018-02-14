import pandas, xlrd, random, math
#COLLEGE BASEBALL SEASON SIMULATOR

def run_game(home, away, win_prob_h, win_prob_a):
    roll = random.random()
    if win_prob_h >= win_prob_a:
        larger = win_prob_h
        lteam = home
        steam = away
    else:
        larger = win_prob_a
        lteam = away
        steam = home
    
    if roll <= larger:
        winner = lteam
        loser = steam
    elif roll > larger:
        winner = steam
        loser = lteam
    else:
        winner = NULL
        loser = NULL

    homeruns = (5.64/(0.5/win_prob_h))
    awayruns = (5.64/(0.5/win_prob_a))

    return winner, loser, homeruns, awayruns

def win_probability(elo1, elo2, homefield):
    if homefield == 1:
        homefield = 45 #Change depending on optimal value
    win_prob = 1 / ((math.pow(10, -((elo1+homefield-elo2)/400)))+1)
    return win_prob

###############
# MAIN PROGRAM
###############

#Importing Tables
xl = pandas.ExcelFile('18schedule.xlsx')
schedule = xl.parse('ncaa_schedule')
elo_ref = xl.parse('elo')

z = 1
k_value = 1.5 #Change to match optimal value

while z <= 100: #Set to desired number of simulations

    #Re-setting Elo values
    elo_ref['18_elo'] = elo_ref['18_elo_static']
    i = 0

    for index, row in schedule.iterrows():
        #Accessing Matchup
        home_team = schedule['Home'][i]
        elo_row = elo_ref.loc[elo_ref['School']==home_team].index[0]
        home_elo = float(elo_ref['18_elo'][elo_row])

        away_team = schedule['Away'][i]
        elo_row = elo_ref.loc[elo_ref['School']==away_team].index[0]
        away_elo = float(elo_ref['18_elo'][elo_row])

        date = str(schedule['Date'][i])
        print('Game #{}' .format(i+1))
        print('{} ({}) @ {} ({}) on {}' .format(away_team, int(away_elo), home_team, int(home_elo), date[:-9]))

        margin = abs(home_elo-away_elo)
        average_elo = (home_elo+away_elo)/2

        #Determining Win Probabilities
        win_prob_home = win_probability(home_elo, away_elo, 1)
        win_prob_away = win_probability(away_elo, home_elo, 0)
        print('{} has a {:.1f}% chance of beating {}' .format(home_team, 100*win_prob_home, away_team))

        #Running Matchup
        winner, loser, homeruns, awayruns = run_game(home_team, away_team, win_prob_home, win_prob_away)
        pointdif = abs(homeruns - awayruns)
        print('{} beat {} by {}\n' .format(winner, loser, int(pointdif)))

        #Count Wins and Losses
        elo_ref.loc[elo_ref['School'] == winner, 'Wins'] += 1
        elo_ref.loc[elo_ref['School'] == loser, 'Losses'] += 1

        #Update Team Elo's and Standings
        if winner == home_team:
            elowin = home_elo
            eloloss = away_elo
        else:
            elowin = away_elo
            eloloss = home_elo

        elo_change = math.log(pointdif+1)*(2.2/(((elowin-eloloss)*0.001)+2.2))*k_value #Formula via 538
            
        elo_ref.loc[elo_ref['School'] == winner, '18_elo'] += elo_change
        elo_ref.loc[elo_ref['School'] == loser, '18_elo'] -= elo_change

        #K Value Testing
        #Finding squared error per game based on k value and home field input, later averaged per test
        #homeresult = schedule['Win'][i]
        #awayresult = 1 - homeresult
        #squared_error = math.pow(win_prob_home - homeresult, 2) + math.pow(win_prob_away - awayresult, 2)
        #schedule.loc[schedule['Game'] == i, 'Squared Error'] = squared_error
        i += 1
    #Measuring average Elo over all simulations
    elo_ref.loc[:, 'avg_elo'] += elo_ref.loc[:, '18_elo']
    z += 1

#Final Update and Export
elo_ref.loc[:, 'Wins'] /= (z-1)
elo_ref.loc[:, 'Losses'] /= (z-1)
elo_ref.loc[:, 'avg_elo'] /= (z-1)
print(elo_ref.sort_values(by=['Wins'], ascending=False))
elo_ref.to_csv('18sim.csv')