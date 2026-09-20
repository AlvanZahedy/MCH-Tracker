import discord
import multiprocessing as mp
import requests
import time

if True: #Variables
  client = discord.Client()
  APIKEY = '929a1834-d1fb-4d8b-8ea7-5b25ac1c5046'
  TOKEN = open('token.txt', 'r').read
  logs = client.get_channel(888413643383910410)
  Tracking_Channel = client.get_channel(882685351729188924)

class Tracker:
  
  def get_ws(self,gamemode,apikey,name,Response):
    try:
      winstreak = Response["player"]["stats"]["Bedwars"][gamemode]
      return winstreak
    except: print(Response)

  def get_info(self,Name):
    Response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{Name}").json()
    dicti = {
    "Name": Response['name'],
    "UUID": Response['id'],}
    return dicti

  def get_played(self,apikey,name,Response):
    Played = Response["player"]["stats"]["Bedwars"]["games_played_bedwars_1"]
    return Played

  def add(self,name):
    a = Tracker()
    Name = a.get_info(name)["Name"]
    with open('Players.txt', 'r+') as players:
      cplayers = players.readlines()
      if Name in cplayers: print('Failed')
      else: a.track(Name)

  def remove(self,name):
    c = Tracker()
    Name = c.get_info(name)["Name"]
    del db["Players"][Name]

  def code(self,nAme):
    b = Tracker()
    UUID = str(b.get_info(nAme)["UUID"])
    NAME = str(b.get_info(nAme)["Name"])
    if True: #Starting Def's
      response = requests.get(f'https://api.hypixel.net/player?key={APIKEY}&uuid={UUID}').json()
      Storage1 = b.get_ws("winstreak",APIKEY,UUID,response)
      fours = b.get_ws("four_four_winstreak",APIKEY,UUID,response)
      threes = b.get_ws("four_three_winstreak",APIKEY,UUID,response)
      twos = b.get_ws("eight_two_winstreak",APIKEY,UUID,response)
      ones = b.get_ws("eight_one_winstreak",APIKEY,UUID,response)
      Jebait1 = b.get_played(APIKEY,UUID,response)
      gamemode = "N/A"
      prevgm = "N/A"
      nextgm = "N/A"
    while True:
      response = requests.get('https://api.hypixel.net/player?key=' + APIKEY + '&uuid=' + UUID).json()
      time.sleep(1.5)
      Storage2 = b.get_ws("winstreak",APIKEY,UUID,response)
      if Storage1 == Storage2: 
        print("No change has been detected! Current WS: " + str(Storage2))
      else:
        if True:
          fourss = b.get_ws("four_four_winstreak",APIKEY,UUID,response)
          threess = b.get_ws("four_three_winstreak",APIKEY,UUID,response)
          twoss = b.get_ws("eight_two_winstreak",APIKEY,UUID,response)
          oness = b.get_ws("eight_one_winstreak",APIKEY,UUID,response)
          if fourss != fours:
            gamemode = "4v4v4v4"
            nextgm = fourss
            prevgm = fours
          elif threess != threes:
            gamemode = "3v3v3v3"
            nextgm = threess
            prevgm = threes
          elif twoss != twos:
            gamemode = "Doubles"
            nextgm = twoss
            prevgm = twos
          elif oness != ones:
            gamemode = "Solos"
            nextgm = oness
            prevgm = ones
        if Storage1 > Storage2:
          LosingMessage = str('<:l1:881935132162932766><:l2:881935154476613632><:l3:881935174064021534><:l4:881935203709382696><:l5:881935224198561823>') + NAME + "'s Overall Winstreak: " + str(Storage1) + " -> " + str(Storage2) + " " + str(gamemode) + (" Winstreak: " ) + str(prevgm) + (" -> ") + str(nextgm)
          print("game ended (man lost)")
          print(LosingMessage)
          Storage1 = Storage2
        if Storage1 < Storage2:
          WinningMessage = str("<:v1:881934667748634624><:v2:881934703433773168><:v3:881934723763556433><:v4:881934739269894184> ") + NAME + "'s Overall Winstreak: " + (" ") + str(Storage1) + " -> " + str(Storage2) + str(gamemode) + (" Winstreak: " ) + str(prevgm) + (" -> ") + str(nextgm)
          print("game ended (man won WOOOOO VICTORY ROYALE)")
          print(WinningMessage)
          Storage1 = Storage2
      time.sleep(1.5)
      Jebait2 = b.get_played(APIKEY,UUID,response)
      if Jebait1 == Jebait2:
        print("Games played is still same! Current games played is " + str(Jebait2))
      else:
        StartingMessage = "<:s1:882292174505529384><:s2:882292193476345926><:s3:882292216234639444><:s4:882292237621428245> " + NAME + "'s game has started! " + "(" + gamemode + ")"
        print(StartingMessage)
        Jebait1 = Jebait2

  def first_track(self):
    b = Tracker()
    global Process_dict
    global code
    Process_dict = {}
    for person in db["Players"]:
      print(person)
      process = mp.Process(target=b.code,args=[person])
      process.start()
      NAMe = str(b.get_info(person)["Name"])
      Process_dict[NAMe] = process
    print('Complete!')

  def track(self,name):
    b = Tracker()
    process = mp.Process(target=b.code,args=[name])
    NAMe = str(b.get_info(name)["Name"])
    Process_dict[NAMe] = process
    process.start()

pa = Tracker()
pa.first_track()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user: return

  if message.content.startswith("t.add "): #Add Player
    t = Tracker()
    raw = message.content.split("t.add ", 1)[1]
    name = str(t.get_info(raw)["Name"])
    t.add(name)
    await message.channel.send(f'Added {name} to the tracker!')

  if message.content.startswith("t.remove"): #Remove Player
    t = Tracker()
    raw = message.content.split("t.remove ", 1)[1]
    name = str(t.get_info(raw)["Name"])
    process = Process_dict.pop(name)
    process.terminate()
    t.remove(name)
    await message.channel.send(f'Removed {name} from the tracker!')

  if message.content.startswith('t.list'):
    print(db['Players'])
    a = 0
    Desc = ""
    for key in db['Players']:
      a += 1
      if a == 1:
        Ti = f'Currently Tracking {a} player!'
        Desc += f'{a}. {key}'
      else:
        Ti = f'Currently tracking {a} players!'
        Desc += f'\n{a}. {key}'
    if a == 0:
      Ti = 'Currently not tracking anyone :('
      Desc = ''
    e = discord.Embed(
      title = Ti,
      description = Desc,
      colour = discord.Colour.blue()
      )
    await message.channel.send(embed=e)
    print(Desc)

client.run(TOKEN)