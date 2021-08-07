# Modules requiring install:
# urllib3
# BeautifulSoup4
# PyPresence
# requests

from urllib.request import urlopen                      #
from urllib.error import URLError                       #
from bs4 import BeautifulSoup                           # web scraper to get info from wMAN webserver
from pypresence import Presence                         # set up RPC
from pypresence.exceptions import InvalidPipe           # handle if Discord is not found to be open
from pypresence.exceptions import InvalidID             # ?? handles some Discord exception
import time                                             # used for "time elapsed" functionality
import requests                                         # used to test ping a local IP address
from requests.exceptions import ConnectionError         # handle if IP address does not host a webserver
import socket                                           # used to get PC's IP address
import re                                               # used for regular expressions, trimming scraped webpage info

# __________ __________
tempSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tempSock.connect(("8.8.8.8", 80))
PCip = tempSock.getsockname()[0]                                   # machines local IP address
tempSock.close()

splitIP = PCip.split(".")
octetFour = 1                                                # assume all home modems use ".1" as the default gateway


def readIP():
    try:
        with open('wMAN ip address.txt') as file:
            savedIP = file.read()
            print("IP saved in file is: ", savedIP)
            file.close()
            isWebman(savedIP)
    except FileNotFoundError:
        getIP()


def getIP():
    print("Program can find address of wMAN server automatically, however this process take awhile,\n"
          "would you prefer to enter the IP address manually, or start an automatic search?\n")
    global mode
    mode = input("Please enter either Manual (m) or Automatic (a): ")
    options = {"A", "a", "Auto", "auto", "Automatic", "automatic"}
    if mode in options:
        print("Automatic search begins, please wait.")
        print(splitIP[0]+"."+splitIP[1]+"."+splitIP[2]+".__")
        findIP()
    else:
        Mip = input("Enter PS3's IP address: ")
        isWebman(Mip)


def findIP():
    global octetFour                    # could restructure so global variable isn't needed?
    octetFour += 1                      # if restructured, findIP() would be called with octectFour+1
    if int(octetFour) < 255:
        Aip = splitIP[0] + "." + splitIP[1] + "." + splitIP[2] + "." + str(octetFour)
        try:
            requests.get("http://"+Aip)
            isWebman(Aip)
        except requests.ConnectionError:
            print("(",octetFour,")",end="")
            findIP()
    else:
        print("Automatic search process failed")
        getIP()


def isWebman(ip):
    global mode
    try:
        requests.get("http://" + ip)
        print("\nHost found at: ", ip, end=" ")
        quote_page = "http://" + ip
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(quote_page, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        pageTitle = soup.find('title')
        pageTitle = str(pageTitle)
        pageTitle = pageTitle.split()
        if pageTitle[0] == "<title>wMAN":
            print("is wMAN")
            saveIP(ip)
        else:
            print("not wMAN")
            options = {"A", "a", "Auto", "auto", "Automatic", "automatic"}
            if mode in options:
                findIP()
            else:
                getIP()
    except requests.ConnectionError:
        print("No web server on: ", ip)
        getIP()


def saveIP(ip):
    global gIP
    file = open("wMAN ip address.txt", "w+")
    file.write(ip)
    file.close()
    gIP = ip


def findDiscord():
    try:
        RPC.connect()  # connect() can only be ran once per session
        print("findDiscord(): found")
    except InvalidPipe:  # handles if discord is not running on PC
        print("findDiscord(): !not found!")
        time.sleep(10)
        findDiscord()


readIP()
client_id = "780389261870235650"
RPC = Presence(client_id)
findDiscord()
timer = time.time()


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
      Fan = re.search(':  (.+?)%', HTMLFan)
      Fan = Fan.group(0)
      Fan = "Fan Speed" + Fan

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
      quote_page = 'http://' + gIP + '/cpursx.ps3?/sman.ps3'
      try:
            page = urlopen(quote_page)
            print("getPage(): webman server found, continuing")
            soup = BeautifulSoup(page, 'html.parser')
      except URLError:
            print("getPage(): webman server not found, waiting", hang_time, "seconds before retry")
            RPC.clear()
            time.sleep(hang_time)
            getPage()

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