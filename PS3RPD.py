# Modules requiring install:
# urllib3
# BeautifulSoup4
# PyPresence
# requests

import socket
import requests
from bs4 import BeautifulSoup
from pypresence import Presence
from pypresence import InvalidPipe
import time
from pypresence import InvalidID
from urllib.request import urlopen
from urllib.error import URLError
import re


class PrepWork(object):
    def __init__(self):
        self.mode = "m"
        self.octetFour = 0
        self.splitIP = []
        self.options = {"A", "a", "Auto", "auto", "Automatic", "automatic"}
        self.ip = None
        self.client_id = "780389261870235650"   # default client_id is my own
        self.sleep_time = "35"                  # default sleep time is 35 seconds
        self.temperatureBoolean = "True"        # default to show temperature is True
        self.separateCovers = "False"           # default to have separate PSX and PS2 covers is False
        self.resetTimeOnGameChange = "True"
        self.RPC = None

    def getParams(self):
        try:
            file = open("PS3RPDconfig.txt", "r")
            lines = file.readlines()
            # print(lines)  # DEBUGGING
            file.close()
            try:
                self.ip = lines[0]  # first line in file (the IP address)
                self.ip = self.ip.split(": ")  # split so ip[0] = "IP: ", ip[1] = (whatever the PS3's ip is)
                self.ip = self.ip[1]  # make ip the address, not "IP: "

                self.client_id = lines[1]  # second line in file (the client id)
                self.client_id = self.client_id.split(": ")  # split so client_id[0] = "ID: ", client_id[1] = (whatever id is)
                self.client_id = self.client_id[1]  # make client_id the string of numbers, not "ID: "
                self.client_id = self.client_id.rstrip("\n")    # I have no idea why this particular line has a \n

                self.sleep_time = lines[2]  # third line in file (the sleep time)
                self.sleep_time = self.sleep_time.split(": ")  # split so [0] = "Refresh time: ", [1] = (whatever value is)
                self.sleep_time = self.sleep_time[1]  # make sleep_time the number
                self.sleep_time = int(self.sleep_time)
                if self.sleep_time < 15:
                    self.sleep_time = 15

                self.temperatureBoolean = lines[3]  # fourth line in file (the boolean of whether to show temps or not)
                self.temperatureBoolean = self.temperatureBoolean.split(": ")  # split so [0] = "Show temperatures: ", [1] = (value)
                self.temperatureBoolean = self.temperatureBoolean[1]  # make temperatureBoolean the value
                self.temperatureBoolean = self.temperatureBoolean.rstrip("\n")  # remove newline from text

                self.separateCovers = lines[4]      # fifth line in file (boolean of whether to show a shared cover or not)
                self.separateCovers = self.separateCovers.split(": ")    # split so [0] = "Individual PS2&PSX covers: ", [1] = (value)
                self.separateCovers = self.separateCovers[1]
                self.separateCovers = self.separateCovers.rstrip("\n")

                self.resetTimeOnGameChange = lines[5]
                self.resetTimeOnGameChange = self.resetTimeOnGameChange.split(": ")
                self.resetTimeOnGameChange = self.resetTimeOnGameChange[1]

                self.isWebman(self.ip)
            except IndexError:
                print("ERROR WITH CONFIG FILE, PLEASE DELETE IT")
                exit(0)
        except FileNotFoundError:
            print("config file not found\n")
            self.getIP()

    def getIP(self):
        print("This program can find the address of your PS3 automatically, however this process takes a while,\n"
              "would you prefer to enter the IP address manually, or start an automatic search?\n")
        self.mode = input("Please enter either manual (M) or Automatic (A): ")
        if self.mode in self.options:
            print("Automatic search begins, please wait.")
            tempSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tempSock.connect(("8.8.8.8", 80))
            PCip = tempSock.getsockname()[0]
            tempSock.close()
            self.splitIP = PCip.split(".")
            print(self.splitIP[0] + "." + self.splitIP[1] + "." + self.splitIP[2] + ".___")
            self.findIP()
        else:
            self.ip = input("Enter PS3's IP address: ")
            self.isWebman(self.ip)

    def findIP(self):
        self.octetFour += 1
        if self.octetFour < 254:
            self.ip = self.splitIP[0] + "." + self.splitIP[1] + "." + self.splitIP[2] + "." + str(self.octetFour)
            try:
                requests.get("http://" + self.ip)
                print("\nHost found at: ", self.ip, end=" ")
                self.isWebman(self.ip)
            except requests.ConnectionError:
                print("(", self.octetFour, ")", end="")
                self.findIP()
        else:  # called if all requests in range fail to find wMAN server
            print("Automatic search process failed")
            self.getIP()

    def isWebman(self, ip):  # is only called if a web server is on the address
        try:  # request needed to ensure server doesn't error out
            ip = ip.rstrip("\n")  # remove newline from text
            # print(ip)                                     # DEBUGGING
            requests.get("http://" + ip)
            quote_page = "http://" + ip
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(quote_page, headers=headers)  # handles 401, 404, etc, errors
            soup = BeautifulSoup(response.text, "html.parser")

            pageTitle = str(soup.find('title'))
            if 'wMAN' in pageTitle or 'webMAN' in pageTitle:
                print("is wMAN")
                self.saveIP(ip)
            else:
                print("not wMAN, page reports: ", pageTitle, '\nIf you believe this is an error, please contact the developer.\n')
                if self.mode in self.options:
                    self.findIP()
                else:
                    self.getIP()
        except requests.ConnectionError as e:
            print("Some error occurred on input address, did your PS3's IP address change?\n")
            print(e, "\n")
            self.getIP()

    def saveIP(self, ip):
        file = open("PS3RPDconfig.txt", "w+")  # w+ creates the file if it is missing
        file.write("IP: ")
        file.write(ip)  # ip changes based on what program finds/is entered

        file.write("\nID: ")
        file.write(str(self.client_id))  # default client_id is my own

        file.write("\nRefresh time(seconds): ")
        file.write(str(self.sleep_time))  # default refresh time is 35 seconds, minimum 15

        file.write("\nShow temperatures: ")
        file.write(str(self.temperatureBoolean))  # default is true, anything else will be false

        file.write("\nIndividual PS2&PSX covers: ")
        file.write(str(self.separateCovers))

        file.write("\nReset time elapsed on game change: ")
        file.write(str(self.resetTimeOnGameChange))
        file.close()

    def findDiscord(self):
        self.RPC = Presence(self.client_id)
        while True:         # use infinite loop instead of calling self to avoid maximum recursion depth
            try:
                self.RPC.connect()
                print("findDiscord():       found")
                break
            except InvalidPipe:
                print("findDiscord():       !not found!")
                time.sleep(10)


class GatherDetails(object):
    def __init__(self):
        self.soup = None                # HTML of webmanMOD page
        self.CPUandRSX = None           # Extracted temperatures
        self.ps3Game = None             # Extracted ps3 game name
        self.gameName = None            # Name of either mounted PSX/PS2 game, or name of open PS3 game
        self.gameType = None            # string containing whether game is PSX, PS2, PS3, etc.
        self.isPS3 = True               # boolean used to make PSX & PS2 games have only 1 cover
        self.gameImage = None           # Name of validated gameName
        self.titleID = None             # titleID of PS3 games (BLUS, NPUB, etc)

    def getPage(self):
        ip = setup.ip.rstrip("\n")  # remove newline from text
        quote_page = "http://" + ip + "/cpursx.ps3?/sman.ps3"
        while True:         # use infinite loop instead of calling itself to avoid maximum recursion depth
            try:
                page = urlopen(quote_page)
                print("getPage():       webman server found, continuing")
                self.soup = BeautifulSoup(page, "html.parser")
                break
            except URLError:
                print("getPage():       webman server not found, waiting", setup.sleep_time, "seconds before retry")
                if self.gameType != "mount.ps3/dev_hdd0/PS2ISO":            # handles webmanMOD going down when a PS2 game is open
                    setup.RPC.clear()
                time.sleep(float(setup.sleep_time))

    def getThermals(self):          # gets temperature from webmanMOD
        HTMLCPUandRSX = str(self.soup.find("a", href="/cpursx.ps3?up"))
        CPUtemp = re.search('CPU(.+?)C', HTMLCPUandRSX).group(0)
        RSXtemp = re.search('RSX(.+?)C', HTMLCPUandRSX).group(0)

        self.CPUandRSX = CPUtemp + " | " + RSXtemp
        print("getThermals():   ", self.CPUandRSX)

    def getGameInfo(self):          # gets name of open/mounted game or homebrew from webmanMOD
        # As Todd Howard said, "it just works". This really should be broken down into multiple functions
        # The following code will first check for if a PS3 game is mounted (ps3Game), which is displayed separately from other games in webmanMOD's HTML,
        # If found, that means a homebrew/PS3 game must be open, display that as the presence
        # If not found, move onto gameType, and check if a different type of game is mounted
        # If one is, display it as the presence
        # If one is not, assume the user is on the XMB and display that
        self.titleID = str(self.soup.find("a", href=True, text=True, target="_blank"))      # find titleID of PS3 games
        if self.titleID != "None":                                                         # will only detect PS3 games
            self.titleID = re.search('>([^>]*)<', self.titleID).group(1)                    # extract titleID from surrounding HTML (used for gameImage and pypresence large_text)
            self.isPS3 = True
            self.ps3Game = str(self.soup.find("a", href=True, text=True, target="_blank").find_next_sibling())
            self.ps3Game = self.ps3Game.replace("\n", " ")
            self.ps3Game = self.ps3Game.replace("&amp;", "&")
            self.ps3Game = re.search('\?q=([^>]*)\">', self.ps3Game)
            # print(self.ps3Game)           # DEBUGGING
            self.ps3Game = self.ps3Game.group(1)
            print("getGameInfo():   ", self.gameName)
            self.gameName = self.ps3Game
        else:                                           # If no PS3 game is open, assume user is on the XMB
            self.gameName = "XMB"
            print("getGameInfo():   ", self.gameName)

            self.gameType = str(self.soup.find('a', href=re.compile('mount(.+?)+')))
            self.gameType = re.search('mount.ps3/dev_hdd0/(?:GAMES|PS2ISO|PSXISO|PSPISO|PS3ISO)', self.gameType)  # honestly could probably remove "GAMES" and "PS3ISO", but it woks fine the way it is
            if self.gameType is not None:
                try:
                    self.gameType = self.gameType.group(0)
                except AttributeError:
                    print("[Timing Error]")
                    exit(1)             # this should never be reached in the release of the script, but is kept for my own sanity
                # some game must be mounted if the code reaches here
                if self.gameType != "mount.ps3/dev_hdd0/GAMES" and self.gameType != "mount.ps3/dev_hdd0/PS3ISO":  # ensure a PS3 game is not mounted
                    self.isPS3 = False
                    otherGame = str(self.soup.find("a", href=re.compile('mount(.+?)+')))
                    otherGame = re.search('>(.+?)<', otherGame)         # name of game/file mounted
                    if otherGame is not None:
                        otherGame = otherGame.group(1)          # excludes ">" "<"
                        self.gameName = otherGame               # set presence variable to game/file mounted
                        cleanUp = ["\n", "(USA)", ".bin", ".BIN", ".iso", ".ISO", ".pkg", ".PKG", "(EUR)", "(JAP)", "(usa)", "(eur)","(jap)"]   # I don't know how many of these will actually
                        # ever be used, but it should handle a majority of games people play?
                        for i in range(len(cleanUp)):
                            self.gameName = self.gameName.replace(cleanUp[i], "")
                        print("getGameInfo():   ", self.gameName)

    def validate(self):         # validates the game's name for Discord's art asset naming conventions (allows images to display)
        if self.isPS3 is False:         # PS2 and PSX games do not have a titleID in webman, so use the name of game
            self.gameImage = self.gameName
        else:
            self.gameImage = self.titleID   # PS3 games should use the titleID as the image name so more languages are supported

        if self.isPS3 is False and setup.separateCovers == "False" or self.isPS3 is False and setup.separateCovers == "false":
            if self.gameType == "mount.ps3/dev_hdd0/PSXISO":
                self.gameImage = "psx"
            elif self.gameType == "mount.ps3/dev_hdd0/PS2ISO":
                self.gameImage = "ps2"
            else:
                self.gameImage = "xmb"

        self.gameImage = self.gameImage.lower()
        # Following lines needed only for PS1 and PS2 games as PS3 uses titleID
        self.gameImage = self.gameImage.replace(" ", "_")                   # spaces (" ") are not allowed in image name
        self.gameImage = self.gameImage.replace("&amp;", "")               # "amp" would not be removed without this
        self.gameImage = re.sub("[\W]+", "", self.gameImage)                # removes any non-letter, digit, or underscore
        self.gameImage = self.gameImage[:32]                                # max 32 characters

        print("validate():      ", self.gameImage)


setup = PrepWork()
setup.getParams()  # goes through all defined functions in PrepWork(), minus findDiscord()
setup.findDiscord()

details = GatherDetails()
previousGameTitle = ""
timer = time.time()


while True:
    details.getPage()
    details.getGameInfo()
    if setup.temperatureBoolean == "True" or setup.temperatureBoolean == "true":
        if details.isPS3 is False:
            details.CPUandRSX = "　　"        # do not display temperature regardless of user preference as it is not correct when playing PS2 games
        else:
            details.getThermals()
    if details.gameName != previousGameTitle:
        previousGameTitle = details.gameName
        details.validate()                  # validate only needs to run if the game/app has been changed
        if setup.resetTimeOnGameChange == "True" or setup.resetTimeOnGameChange == "true":
            timer = time.time()
    else:
        print("prev validate(): ", details.gameImage)
    try:
        setup.RPC.update(details=details.gameName, state=details.CPUandRSX, large_image=details.gameImage, large_text=details.titleID, start=timer)
    except(InvalidPipe, InvalidID):
        setup.findDiscord()
    time.sleep(int(setup.sleep_time))
    print("\n")

# NOTES:
# script will only read external config file once, any changes made won't be reflected until script is restarted
