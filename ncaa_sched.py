import json, requests, csv, pandas

def get_data(schedule):
    num_games = 0
    x = True
    z = 0
    while x is True:
        try:
            game = schedule['scoreboard'][0]['games'][num_games]
            num_games = num_games + 1
        except:
            break

    for z in range(0, num_games):
        date = schedule['scoreboard'][0]['games'][z]['startDate']
        home = schedule['scoreboard'][0]['games'][z]['home']['nameRaw']
        away = schedule['scoreboard'][0]['games'][z]['away']['nameRaw']
        gamedict = {'Date': date, 'Home': home, 'Away': away}
        datedata.append(gamedict)
    return datedata

###############
# MAIN PROGRAM
###############

all_data = []
datedata = []
datelist = []
datem = ["02", "03", "04", "05"]
dated = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
for i in range(0,len(datem)):
    for j in range(0, len(dated)):
            date = datem[i]+"/"+dated[j]
            datelist.append(date)


for i in range(0, len(datelist)):
    url1 = "https://data.ncaa.com/jsonp/scoreboard/baseball/d1/2018/"
    url3 = "/scoreboard.html?callback=ncaaScoreboard.dispScoreboard"
    url = url1+str(datelist[i])+url3
    print(url)
    try:
        response = requests.get(url)
        schedule = response.text[30:-2]
        schedule = json.loads(schedule)
        all_data = get_data(schedule)
    except:
        print("No Games Found")
    
all_data_frame = pandas.DataFrame(all_data)
print(all_data_frame)
all_data_frame.to_csv('ncaa_schedule.csv')
