import os
import time
import requests
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def sortscore(board):
    changes=1
    while changes>0:
        changes=0
        for pos in range(len(board)-1):
            player=board[pos][0]
            score=board[pos][1]
            if board[pos+1][1]>score:
                board[pos][0]=board[pos+1][0]
                board[pos][1]=board[pos+1][1]
                board[pos+1][0]=player
                board[pos+1][1]=score
                changes=changes+1
    return board

def boardexport(path,export,data,xoffset):
    img = Image.open(path)
     
    Draw = ImageDraw.Draw(img)
    if os.path.exists(export):
        os.remove(export)
    if data==[]:
        print("No data for", path)
        return
    
    if len(data)>=1: #1st
        font = ImageFont.truetype(r'./Norwester 400.otf',100)
        Draw.text((330, 220), str(data[0][0]), font=font, fill=(255, 255, 255))
        Draw.text((1010+xoffset, 220), str(data[0][1]), font=font, fill=(255, 255, 255))
    if len(data)>=2: #2nd
        font = ImageFont.truetype(r'./Norwester 400.otf',80)
        Draw.text((270, 395), str(data[1][0]), font=font, fill=(64, 57, 57))
        Draw.text((870+xoffset, 395), str(data[1][1]), font=font, fill=(64, 57, 57))
    if len(data)>=3: #3rd
        font = ImageFont.truetype(r'./Norwester 400.otf',70)
        Draw.text((220, 530), str(data[2][0]), font=font, fill=(255, 255, 255))
        Draw.text((770+xoffset, 530), str(data[2][1]), font=font, fill=(255, 255, 255))
    if len(data)>=4: #4th
        font = ImageFont.truetype(r'./Norwester 400.otf',60)
        Draw.text((190, 655), str(data[3][0]), font=font, fill=(255, 255, 255))
        Draw.text((760, 655), str(data[3][1]), font=font, fill=(255, 255, 255))
    if len(data)>=5: #5th
        font = ImageFont.truetype(r'./Norwester 400.otf',60)
        Draw.text((190, 775), str(data[4][0]), font=font, fill=(255, 255, 255))
        Draw.text((760, 775), str(data[4][1]), font=font, fill=(255, 255, 255))
    if len(data)>=6: #6th
        bottomlist="6.  "+str(data[5][0])+"   "+str(data[5][1])
        if len(data)>=7: #7th
            bottomlist=bottomlist+"        7.  "+str(data[6][0])+"    "+str(data[6][1])
        if len(data)>=8: #8th
            bottomlist=bottomlist+"        8.  "+str(data[7][0])+"    "+str(data[7][1])
        font = ImageFont.truetype(r'./Norwester 400.otf',40)
        Draw.text((150, 900), bottomlist, font=font, fill=(255, 255, 255), align ="center")
    if len(data)>=9: #9th
        bottomlist="9.  "+str(data[8][0])+"    "+str(data[8][1])
        if len(data)>=10: #10th
            bottomlist=bottomlist+"        10.  "+str(data[9][0])+"    "+str(data[9][1])
        font = ImageFont.truetype(r'./Norwester 400.otf',40)
        Draw.text((350, 1000), bottomlist, font=font, align ="center", fill=(255, 255, 255))

    img.save(export)
    print("Exported "+export)

def getLeaderboard(app,period,Type): #Get leaderboard from ggleap API
    querystring = {"App":app,"Period":period,"Type":Type,"CenterType":"All"}
    response = requests.request("GET", "https://api.ggleap.com/beta/leaderboards/client-leaderboard", headers={"Content-Type": "application/json", "Authorization": JWT}, params=querystring)
    response=response.json()
    trimmed=[]
    for pos in range(len(response['Items'])):
        names=response['Items'][pos]['Username']
        trimmed.append([names[:13], int(response['Items'][pos]['Score'])])
    return trimmed







#Start of loop

print("Make sure Amazon Photos desktop app is open!")

while 1:
    #Auth
    key="yourkeyhere"

    url = "https://api.ggleap.com/beta/authorization/public-api/auth"
    payload = "{\n  \"AuthToken\": \""+key+"\"\n}"
    headers = {"Content-Type": "application/json-patch+json"}
    response = requests.request("POST", "https://api.ggleap.com/beta/authorization/public-api/auth", data=payload, headers=headers)
    JWT=response.text[8:len(response.text)-2]

    smash=[["Chronos", ""],
           ["KRU / Smirk", ""],
           ["CSU / Robber", ""],
           ["AciD", ""],
           ["Feller", ""],
           ["KRU / Shoe", ""],
           ["FoCo  Solax", ""],
           ["Super", ""],
           ["KRU / CarbonCopies", ""],
           ["ICYoyo", ""]]
           
    period="Month" #Time period for the leaderboards can be: Month, Week, Day
    fortnite=getLeaderboard("fortnite",period,"Center") #Get leaderboard for fortnite
    apex=getLeaderboard("apex",period,"Center") #Get leaderboard for apex
    lol=getLeaderboard("lol",period,"Center") #Get leaderboard for league of legends
    valorant=getLeaderboard("valorant",period,"Center") #Get leaderboard for valorant

    boardexport(r'./blankboards/fortnite_bg.png',r'./Leaderboards/fortnite.png',fortnite,150)
    boardexport(r'./blankboards/apex_bg.png',r'./Leaderboards/apex.png',apex,50)
    boardexport(r'./blankboards/lol_bg.png',r'./Leaderboards/lol.png',lol,0)
    boardexport(r'./blankboards/valorant_bg.png',r'./Leaderboards/valorant.png',valorant,20)

    print("Sleeping...")
    time.sleep(3600)
