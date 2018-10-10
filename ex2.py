#imports all necessary libraries for the function to run
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
#creates function
def get_schema():
#gets url's from input.txt and puts it into a list
    print("Reading file...")
    fname = "input.txt"
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    pile = []
    data = []
    index = 1
#for every url in the list, it get's the html
    for i in content:
        print("Getting row:", index)
        index += 1
        x = requests.get(i)
        soup = BeautifulSoup(x.content, "lxml")
    #for every html it finds the div content
        pile = soup.find_all(attrs={'class': re.compile(r"^user-information__achievements-data$")})
        title = soup.find("meta",  property="og:title")
        name = str(title)[38:-23]
    #gets numbers
        pile = ''.join([line.strip() for line in str(pile)])
        pile = pile.replace(",", "")
        pile = re.findall(r'>([0-9]*)<.div>', pile)
    #append data as dictionary to the data list defined earlier
        dicto = {
            "Name" : name,
            "Badges" : int(pile[0]),
            "Points" : int(pile[1]),
            "Trails" : int(pile[2])
            }
        data.append(dicto)
#Create pandas DataFrame
    df = pd.DataFrame(data)
    df = df[['Name', 'Points', 'Badges', 'Trails']]
#Create panda Dataframes ranked by Points and Badges
    df_points = df.sort_values(by=['Points'], ascending=False)
    df_badges = df.sort_values(by=['Badges'], ascending=False)
    print(df_points)
#Write both dataframes to Excel in two seperate sheets
    print("Writing dataframe to TrailHead_Ranking.xlsx...")
    writer = pd.ExcelWriter('TrailHead_Ranking.xlsx', engine='xlsxwriter')
    df_points.to_excel(writer, 'Ranked by Points')
    df_badges.to_excel(writer, 'Ranked by Bages')
    writer.save()
    print("Done")
#calls function
get_schema()