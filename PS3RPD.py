# Modules requiring install:
# urllib3
# BeautifulSoup4
# PyPresence
# requests

from urllib.request import urlopen                  # open page for BeautifulSoup
from urllib.error import URLError

from bs4 import BeautifulSoup                       # wMAN page scraping

from pypresence import Presence                     # discord rich presence handler
from pypresence.exceptions import InvalidPipe       # error handling
from pypresence.exceptions import InvalidID         # error handling

import time                                         # time elapsed

import requests                                     # used to handle error 404 with BeautifulSoup
from requests.exceptions import ConnectionError

import socket                                       # get PC's IP address to use as a base for PS3 IP

import re                                           # regular expressions for getting CPU, RSX, and FAN values

# __________wMAN server IP finder__________
# 1. Get PC's IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
PCIp = s.getsockname()[0]                             # the PC's local IP address
s.close()
# print("PC's IP is: ", PCIp)                         #debugging

# 2. Split variable to be octet editable
splitIP = PCIp.split(".")
octetFour = 2                                         # starting value of 2 since 1 should be users modem/router

print("Program can find IP address of wMAN server automatically, however this process takes a while,\n"
      "would you prefer to enter the IP address manually, or to continue with auto search?")


def getIP():
      mode = input("\nPlease choose either Manual (m) or Automatic (a): ")
      if mode == "A" or mode == "a" or mode == "Auto" or mode == "auto" or mode == "Automatic" or mode == "automatic":

            print("Automatic search begin (20 seconds per search)")
            print(splitIP[0] + "." + splitIP[1] + "." + splitIP[2] + ".__ ")
            findIP()
      else:
            mIP = input("Enter PS3's IP address: ")
            manualIPTest(mIP)


def findIP():                 # test of each number takes 21 seconds assuming no host found
    global testIP
    global octetFour
    # 3. iterate until title of page is "<title>wMAN
    octetFour = int(octetFour)
    if octetFour <= 255:
          try:
                octetFour = str(octetFour)
                testIP = splitIP[0] + "." + splitIP[1] + "." + splitIP[2] + "." + octetFour
                response = requests.get("http://" + testIP)             # used for exception
                isWebman()

          except requests.ConnectionError as exception:                # only runs if nothing is assigned to that IP
                print("(", octetFour, ")", end=" ")                    # DEBUGGING
                octetFour = int(octetFour)
                octetFour = octetFour + 1
                octetFour = str(octetFour)
                findIP()
    else:
          print("\nAutomatic IP process failed")
          getIP()


def isWebman():
      global testIP
      global octetFour
      global ip
      print("\nHost at IP: ", testIP, end="")  # DEBUGGING
      found = "false"  # boolean to stop search after webman server address found

      quote_page = "http://" + testIP
      headers = {"User-Agent": "Mozilla/5.0"}                           # handles pages that report as error 404
      response = requests.get(quote_page, headers=headers)
      soup = BeautifulSoup(response.text, 'html.parser')

      pageTitle = soup.find('title')
      pageTitle = str(pageTitle)
      pageTitle = pageTitle.split()
      if pageTitle[0] == "<title>wMAN":
            print(" (is wMAN)")
            found = "true"
            ip = testIP

      if found == "false":
            print(" (not wMAN)")
            octetFour = int(octetFour)
            octetFour = octetFour + 1
            findIP()


def manualIPTest(mIP):
      global ip
      print("You entered: ", mIP)
      try:
            response = requests.get("http://" + mIP)              # if manually entered IP is an address
            print("Host found")
            quote_page = "http://" + mIP
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(quote_page, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            pageTitle = soup.find('title')
            pageTitle = str(pageTitle)
            pageTitle = pageTitle.split()
            if pageTitle[0] == "<title>wMAN":
                  print("is wMAN")
                  found = "true"
                  ip = mIP
            else:
                  print("Not wMAN")
                  getIP()

      except requests.ConnectionError as exception:               # if manually entered IP is not an address
            print("Not wMAN")
            getIP()


def findDiscord():
      try:
            RPC.connect()                                         # connect() can only be ran once per session
            print("findDiscord(): found")
      except InvalidPipe:                                         # handles if discord is not running on PC
            print("findDiscord(): !not found!")
            time.sleep(10)
            findDiscord()


getIP()
print("\nWebmanMOD server at: ", ip)
# ____________________

# __________start PyPresence__________
client_id = "780389261870235650"
RPC = Presence(client_id)
findDiscord()
# ____________________
timer = time.time()
# __________check wMAN server status__________

gameType = ""

# __________get values for rich presence__________


def getThermals():
      global CPURSXFan
      HTMLCPUandRSX = soup.find('a', href="/cpursx.ps3?up")
      HTMLCPUandRSX = str(HTMLCPUandRSX)
      CPUtemp = re.search('CPU(.+?)C', HTMLCPUandRSX)
      CPUtemp = CPUtemp.group(0)
      RSXtemp = re.search('RSX(.+?)C', HTMLCPUandRSX)
      RSXtemp = RSXtemp.group(0)

      HTMLFan = soup.find('a', href="/cpursx.ps3?mode")
      HTMLFan = str(HTMLFan)
      Fan = re.search('FAN(.+?)%', HTMLFan)
      Fan = Fan.group(0)

      CPURSXFan = CPUtemp + " | " + RSXtemp + " | " + Fan  # formats string for appearance in rich presence
      print("getThermals(): ", CPURSXFan)
      # ____________________


def getGameInfo():
      global gameName
      global gameType
      gameName = ""
      otherGame = ""
      ps3Game = ""
      ps3GameRegion = soup.find('a', href=True, text=True, target="_blank")
      ps3GameRegion = str(ps3GameRegion)

      if ps3GameRegion != "None":
            ps3Game = soup.find('a', href=True, text=True, target="_blank").find_next_sibling()
            ps3Game = str(ps3Game)
            ps3Game = ps3Game.replace("\n", " ")
            ps3Game = re.search('>(.+[\r\n]?)+<', ps3Game)
            ps3Game = ps3Game.group(1)
            print("getGameInfo() - Game open: ", ps3Game)
            gameName = ps3Game


      gameType = soup.find('a', href=re.compile('mount(.+?)+'))
      gameType = str(gameType)
      gameType = re.search('mount.ps3/dev_hdd0/(?:GAMES|PS2ISO|PSXISO|PSPISO|PS3ISO)', gameType)
      if gameType != "" and gameType != None:
            gameType = gameType.group(0)
            # print("GAMETYPE IS: ", gameType)

      if ps3Game == None or ps3Game == "":
            print("getGameInfo(): XMB")
            gameName = "XMB"

      if ps3Game == None or ps3Game == "":
            gameType = str(gameType)                  # string for if statement
            if gameType != "mount.ps3/dev_hdd0/GAMES" and gameType != "mount.ps3/dev_hdd0/PS3ISO":
                  otherGame = soup.find('a', href=re.compile('mount(.+?)+'))
                  otherGame = str(otherGame)
                  otherGame = re.search('>(.+?)<', otherGame)
                  if otherGame != None:
                        otherGame = otherGame.group(1)
                        print("getGameInfo() - Game mounted: ", otherGame)
                        gameName = otherGame


def validate():
      global gameImage
      global gameName
      gameImage = "none"


      cleanUp = ["\n", "(USA)", ".bin", ".iso", ".pkg", "(EUR)", "(JAP)"]
      for i in range(7):
            gameName = gameName.replace(cleanUp[i], "")
      gameName = gameName.replace("&amp;", "&")


      if gameName != "":
            gameImage = gameName.lower()
            prohibited = ["\n", ":", ";", "®", "™", "&amp", "&", "/", "'", ".", "★"]

            for i in range(11):
                  gameImage = gameImage.replace(prohibited[i], "")
            gameImage = gameImage.replace(" ", "_")
            gameImage = gameImage[:32]
            print("validate(): ", gameImage)


def noImage():
      global gameImage
      if gameImage != "_rebug_toolbox_":
            if gameType == "mount.ps3/dev_hdd0/PS2ISO":
                  gameImage = "ps2"
            if gameType == "mount.ps3/dev_hdd0/PSXISO":
                  gameImage = "psx"

      try:
            with open('implementedImage.txt') as file:
                  line = file.readlines()
                  totalItems = len(line)
                  artPresent = "false"
            file.close()
            for i in range(totalItems):
                  line[i] = line[i].replace("\n", "")
                  if gameImage == line[i]:
                        artPresent = "true"
            if artPresent == "false":
                  gameImage = "unknown_game"
            print("noImage(): ", gameImage)
      except FileNotFoundError:
            print("noImage(): !no external file found!")



def getPage():
      hang_time = 35
      global soup
      # __________access page with information needed__________
      quote_page = 'http://' + ip + '/cpursx.ps3?/sman.ps3'
      try:
            page = urlopen(quote_page)
      except URLError:
            print("getPage(): webman server not found, waiting", hang_time, "seconds before retry")
            time.sleep(hang_time)
            getPage()
      print("getPage(): webman server found, continuing")
      soup = BeautifulSoup(page, 'html.parser')
      # ____________________


while True:
      getPage()
      getThermals()
      getGameInfo()
      validate()
      noImage()

      try:
            RPC.update(details=gameName, state=CPURSXFan, large_image=gameImage, start=timer)
            print("Discord found")
      except (InvalidID, InvalidPipe):
            print("Discord not found")
            findDiscord()
      time.sleep(35)
      print("\n")

# NOTES
# "manualIPTest()" and "isWebman()" could probably be merged
# unable to test PSP games
# If console is turned off while running PS2 game there is no way to detect this and RP stays active


# if implementedImage.txt is not in the same directory as this executable, the program will display all games that have
# images added, however if a game does not have an image, NO image is shown.

# if implementedImage.txt is found, the program will display all games that have images added, as well as have an image
# for games that do not have an image (PS3Discord logo with a "?" overlay)
