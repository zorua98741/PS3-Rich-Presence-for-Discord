import socket                       # for getting PC's IP address
import networkscan                  # requires python 3.7, simple network scanner
import requests                     # for connecting to webpages
from bs4 import BeautifulSoup       # for HTML scraping
from pypresence import Presence     # used for sending data to Discord developer application
from pypresence import InvalidPipe  # used for handling Discord not found on system error
import time                         # used for sleeping script and "time elapsed" functionality
from urllib.request import urlopen  # used for testing if webman server is still available
from urllib.error import URLError   # used for handling webman server going down
import re                           # regular expressions
import hmac                         # used for creating tmdb URL
from hashlib import sha1            # used for creating tmdb URL
from urllib.error import HTTPError  # handle error 404 when opening tmdb page


class ExternalFile(object):         # holds all methods interacting with text document config file
    def __init__(self):
        self.data = []
        self.section = []
        self.s1configVariables = []
        self.s2appIDVariables = []
        self.s2titleIDVariables = []
        self.s3titleIDVariables = []
        self.s3gameNameVariables = []
        self.s3imageVariables = []

    # get all data from external file
    def getData(self):
        try:
            file = open("PS3RPDconfig.txt", "r")        # open file, read-only
            self.data = file.readlines()                     # create list where each item is 1 line from external file
            file.close()

            self.normaliseData()

        except FileNotFoundError:
            print("! config file not found !")
            prepWork.getIPMode()

    # remove formatting from external file
    def normaliseData(self):
        for i in range(len(self.data)):                     # number of items in list
            self.data[i] = self.data[i].rstrip("\n")        # remove newline characters
            try:
                self.data[i] = self.data[i].split(": ", 1)  # split into [0]: [1] (at most 1 time)
                self.data[i] = self.data[i][1]              # makes data[i] "value" instead of "info: value"
            except IndexError:                              # occurs if data[i] does not have a colon in it
                self.data[i] = self.data[i][0]              # makes external file more forgiving of format (":" is not needed on every line due to this code)

        while True:
            try:
                self.data.remove('')                        # remove empty lines
            except ValueError:
                break

        for i in range(len(self.data)):
            if "=" in self.data[i]:                         # create list holding where different sections of data begins
                self.section.append(i)

        for i in range(len(self.data)):
            print(self.data[i])

        self.initialiseConfigVariables()
        self.initialiseDevApps()
        self.initialisePreviouslyResolved()

    # split section 1 of external file into a variable
    def initialiseConfigVariables(self):
        for i in range(self.section[0], self.section[1]-1):    # uses section[] to identify which part of the file to grab data from
            self.s1configVariables.append(self.data[i+1])       # add value to list

        if int(self.s1configVariables[2]) < 15:
            self.s1configVariables[2] = 15                      # minimum value of 15 seconds for the "refresh time" variable
        print("configVariables: ", self.s1configVariables)

    # split section 2 of external file into a variable
    def initialiseDevApps(self):
        for i in range(self.section[1], self.section[2]-1):
            if i % 2 == 0:
                self.s2appIDVariables.append(self.data[i+1])
            else:
                self.s2titleIDVariables.append(self.data[i+1])
        print("devApps: ", self.s2appIDVariables, self.s2titleIDVariables)

    # split section 3 of external file into a variable
    def initialisePreviouslyResolved(self):
        for i in range(self.section[2]+1, len(self.data)):
            line = i
            i = i - self.section[2]-1                       # since self.section[2] is variable, range will change and make modulus operation wrong, fix by bringing "i" back to 0
            if i % 3 == 0:
                self.s3titleIDVariables.append(self.data[line])
            if i % 3 == 1:
                self.s3gameNameVariables.append(self.data[line])
            if i % 3 == 2:
                self.s3imageVariables.append(self.data[line])
        print("previouslyResolved: ", self.s3titleIDVariables, self.s3gameNameVariables, self.s3imageVariables)

    # create and save default data to external file
    def saveData(self):
        file = open("PS3RPDconfig.txt", "w+")           # create external file (opened in write plus mode)
        file.write("==========Persistent Variables==========")
        file.write("\nIP: " + str(prepWork.ip))
        file.write("\nID: " + "780389261870235650")
        file.write("\nRefresh time(seconds): " + "30")
        file.write("\nReset time elapsed on game change: " + "True")
        file.write("\nShow temperatures: " + "True")
        file.write("\n")
        file.write("\n==========Developer Application-to-title IDs==========")
        file.write("\n")
        file.write("\n==========Previously Resolved Games==========")
        file.write("\n")
        file.close()

    # open external file and update ONLY the IP variable
    def updateIP(self):
        pass

    # open external file and add new game to section 3 (also call function to or append new value to s3 variables)
    def addMappedGame(self):
        pass


class PrepWork(object):             # holds all methods run once / are background tasks
    def __init__(self):
        self.ip = None              # PS3 IPv4 address
        self.mode = None            # whether program is manually or automatically given PS3 IP address
        self.ipOptions = ["A", "a", "Auto", "auto", "Automatic", "automatic"]
        self.RPC = None             # pypresence class

    def getIPMode(self):
        print("PS3RPD can run a network scan to automatically find your PS3's IP address. \n"
              "would you prefer to enter the IP address manually, or start an automatic search?")
        self.mode = input("Please enter either manual (M) or automatic (A): ")
        if self.mode in self.ipOptions:
            print("\nAutomatic search begins, please wait.")
            # find PCs local IP address
            tempSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tempSock.connect(("8.8.8.8", 80))
            PCip = tempSock.getsockname()[0]
            tempSock.close()
            print("Local network address for PC is", PCip)

            splitIP = PCip.split(".")                                       # networkscan can't take PC's IP for some reason
            self.getConnectedIPs(splitIP[0] + "." + splitIP[1] + "." + splitIP[2] + ".0")
        else:
            testIP = input("Please enter the PS3's IP address: ")
            if self.isWebman(testIP) is True:                   # isWebman returns boolean
                externalFile.saveData()
            else:
                self.getIPMode()                                # returns False if the IP isn't confirmed as webman server

    # code by nychron#2911, modified by zorua98741
    def getConnectedIPs(self, my_network):
        print("Running network scan.")
        my_network = my_network + "/24"
        my_scan = networkscan.Networkscan(my_network)

        # Run the scan of hosts using pings
        my_scan.run()

        # Display the IP address of all the hosts found
        print("Completed network scan.")
        print(my_scan.list_of_hosts_found)
        self.testConnectedIPs(my_scan.list_of_hosts_found)

    # run through each item in list and call isWebman()
    def testConnectedIPs(self, hosts):
        for i in range(len(hosts)):
            if self.isWebman(hosts[i]) is True:
                externalFile.saveData()
                break
            elif i+1 == len(hosts):
                print("\n! network scan could not find your PS3's IP address !\n")
                self.getIPMode()

    # test if given IP belongs to the PS3 via known HTML in webmanMOD server
    def isWebman(self, testIP):
        print("testing ", testIP)
        try:                                # request needed to ensure server doesn't error out
            testIP = testIP.rstrip("\n")                            # remove newline if present
            quote_page = "http://" + testIP                         # add 'http' to make a valid URL
            headers = {"User-Agent": "Mozilla/5.0"}                 # fixes potential error 404, 401, etc
            response = requests.get(quote_page, headers=headers)    # gets HTML of webmanMOD site
            soup = BeautifulSoup(response.text, "html.parser")      # makes HTML usable? (Don't know how to explain)

            pageTitle = str(soup.find('title'))                     # find <title> tag and its' contents
            if "wMAN" in pageTitle:                     # ! should be changed for more generic test !
                print("is wMAN\n")
                self.ip = testIP                                    # set 'global' ip variable for use in remainder of script
                externalFile.s1configVariables[0] = testIP
                return True
            else:
                print("not wMAN\n")
                if self.mode not in self.ipOptions:                 # return False to testConnectedIPs() only
                    return False
        except requests.ConnectionError as e:
            print("Connection error occurred on input address: \n", e, "\n")
            return False

    # attempt to connect to users Discord application with Application ID from external file
    def findDiscord(self):
        self.RPC = Presence(str(externalFile.s1configVariables[1]))          # use 'ID' variable from external file
        try:
            self.RPC.connect()
            print("findDiscord():       found")
        except InvalidPipe:
            print("findDiscord():       ! not found !")
            time.sleep(15)
            self.findDiscord()                                          # if function fails try again until it succeeds

    # test if given IP address from external file still belongs to webman
    def testPage(self):
        quote_page = "http://" + externalFile.s1configVariables[0] + "/cpursx.ps3?/sman.ps3"    # page containing game name and thermals
        try:
            page = urlopen(quote_page)
            print("testPage():       webman server found, continuing")
        except URLError:
            print("testPage():       ! webman server not found, did your PS3s IP address change? !\n")
            self.getIPMode()

class GatherDetails(object):        # holds all methods extracting data from HTML file
    def __init__(self):
        self.soup = None            # will hold HTML of webmanMOD page
        self.titleID = None         # will hold game's titleID
        self.gameName = None        # will hold game's name
        self.gameImage = None       # will hold game's image
        self.isPS2 = None           # boolean for if PS2 game is mounted or not
        self.CPUandRSX = None       # will hold PS3's temperature (if enabled in external config)

    # gets HTML of webmanMOD page
    def getPage(self):
        quote_page = "http://" + externalFile.s1configVariables[0] + "/cpursx.ps3?/sman.ps3"    # page containing game name and thermals
        try:
            page = urlopen(quote_page)
            print("getPage():       webman server found, continuing")
            self.soup = BeautifulSoup(page, "html.parser")
        except URLError:
            print("getPage():       ! webman server not found, waiting 15 seconds before retry")
#PUT CODE TO HANDLE wMAN SERVER GOING DOWN ON PS2 GAME LAUNCH HERE
            time.sleep(15)
            self.getPage()

    # use available HTML to decide what type of game is open/mounted
    def decideGameType(self):
        #print("PS3 titleID: ", self.soup.find("a", href=True, text=True, target="_blank"))  # serves ALL PS3 and homebrew (uses tmdb for name and image)
        #print(self.soup.find("a", href=True, text=True, target="_blank").find_next_sibling())   # PS3RPDv2 method of finding game name. (for if tmdb fails)
        # \?q([^>]*)\">                                                 REGEX for extracting game name from line above
        #print("dev_bdvd: ", self.soup.find("a", href=re.compile('mount(.+?)')))                     # serves PS2, PSX, PSP(?)

        if self.soup.find("a", href=True, text=True, target="_blank") is not None:
            print("decideGameType():        PS3 game OR homebrew detected, attempting to resolve titleID with tmdb api")
            if self.getTmdbInfo() is False:                                                         # returns False if some error occurs
                self.getWebmanGameName()                                                            # fallback for if titleID is not in tmdb api (will be used primarily for homebrew)

        elif self.soup.find("a", href=re.compile('mount(.+?)')) is not None:
            print("decideGameType():        Some other game detected, using given game name")
            self.getOtherGameInfo()
        else:
            self.gameName = "XMB"
            self.gameImage = "xmb"
            print("decideGameType():        No game is detected, user is on the XMB?")

        gameType = self.soup.find("a", href=re.compile('mount(.+?)'))
        if re.search('(PS2ISO)', str(gameType)) is not None:
            self.isPS2 = True
        else:
            self.isPS2 = False

        self.validate()                                                                             # validate() is called regardless of method used to find game's name

    # use tmdb api to find game name and an image from given titleID
    def getTmdbInfo(self):
        titleID = self.soup.find("a", href=True, text=True, target="_blank")                                        # find HTML line containing titleiD
        titleID = re.search('>([^>]*)<', str(titleID)).group(1)                                                     # remove surrounding HTML so only titleID remains
        self.titleID = titleID                                                                              # set 'global' titleID for use in presence
        titleID = titleID + "_00"                                                                                   # tmdb api requires "_00" for some reason
        Hash = hmac.new(tmdb_key, bytes(titleID, 'utf-8'), sha1).hexdigest().upper()                           # create hash for tmdb URL
        url = "http://tmdb.np.dl.playstation.net/tmdb/" + titleID + "_" + Hash + "/" + titleID + ".xml"             # combine sections of URL to create correct link
        # print(url)                            # DEBUGGING
        try:
            page = urlopen(url).read()          # get xml page
            page = page.decode('utf-8')         # fix utf-8 encoding (remove \xc2\xae and such symbols)
            # print(page)                       # DEBUGGING
            self.gameName = re.search('<name>([^>]*)</name>', page).group(1)                                # set 'global' gameName for use in presence
            self.gameImage = re.search('>([^>]*)</icon>', page).group(1)                                    # set 'global' gameImage for use in presence
            # print("Name: ", self.gameName, "\n", "Image: ", self.gameImage)         # DEBUGGING
            print("getTmdbInfo():       ", self.gameName, self.gameImage)
            return True                                                                                             # nothing happens if return True
        except (HTTPError, AttributeError) as e:
            print("titleID may not be in tmdb database. Error occurred: ", e)
            return False                                                                                            # if return False then call getWebmanGameName()

    # fallback for getTmdbInfo() failing, image will not be found but game name will be
    def getWebmanGameName(self):
        gameName = self.soup.find("a", href=True, text=True, target="_blank").find_next_sibling()       # find HTML line containing game name
        gameName = re.search('\?q=([^>]*)\">', str(gameName)).group(1)                                  # capture the game name from surrounding URL
        self.gameName = gameName                                                                    # set 'global' gameName for use in presence
        print("getWebmanGameName():         ", gameName)

    # use webmanMOD html to extract a game name
    def getOtherGameInfo(self):
        gameName = self.soup.find("a", href=re.compile('mount(.+?)'))                       # find HTML line containing game name
        gameName = re.search('>([^>]*)<', str(gameName)).group(1)                           # capture the game name from surrounding HTML
        self.gameName = gameName                                                        # set 'global' gameName for use in presence
        print("getOtherGameInfo():      ", gameName)

    # fix broken formatting and remove forbidden characters
    def validate(self):
        for i in range(len(junk)):
            self.gameName = self.gameName.replace(junk[i], "")
        self.gameName = self.gameName.replace("&amp;", "&")
        # NOTE: if using Discord dev app, name cannot contain [spaces, uppercase characters, ampersands, longer than 32 characters)
        # shortcut for most of this is re.sub("[^a-zA-Z0-9_]", "", gameImage)
        print("validate():      ", self.gameName)

    # use webmanMOD html to extract a CPU and RSX temperature
    def getThermals(self):
        HTMLCPUandRSX = str(self.soup.find("a", href="/cpursx.ps3?up"))
        CPUtemp = re.search('CPU(.+?)C', HTMLCPUandRSX).group(0)
        RSXtemp = re.search('RSX(.+?)C', HTMLCPUandRSX).group(0)
        self.CPUandRSX = CPUtemp + " | " + RSXtemp
        print("getThermals():       ", self.CPUandRSX)


tmdb_key = bytearray.fromhex('F5DE66D2680E255B2DF79E74F890EBF349262F618BCAE2A9ACCDEE5156CE8DF2CDF2D48C71173CDC2594465B87405D197CF1AED3B7E9671EEB56CA6753C2E6B0')        # known from https://www.psdevwiki.com/ps3/Keys
junk = ["(USA)", "(EUR)", "(JAP)", ".bin", ".iso", "(En,Fr,Es)"]    # holds list of junk PS1/PS2 games can contain (for removal)
true = ["true", "True", "t", "T"]                                   # used so IF statements aren't horribly long

externalFile = ExternalFile()
prepWork = PrepWork()
gatherDetails = GatherDetails()

externalFile.getData()
prepWork.testPage()

prepWork.findDiscord()

while True:             # main program loop of contacting PS3, getting data, and setting the presence
    print("\n")                                                     # formatting
    gatherDetails.getPage()
    gatherDetails.decideGameType()
    if externalFile.s1configVariables[4] in true and gatherDetails.isPS2 is False:
        gatherDetails.getThermals()
    else:
        gatherDetails.CPUandRSX = None
    print("Final output: ", gatherDetails.gameName, " | ", gatherDetails.gameImage, " | ", gatherDetails.CPUandRSX)
    prepWork.RPC.update(details=gatherDetails.gameName, state=gatherDetails.CPUandRSX, large_image=gatherDetails.gameImage, large_text=gatherDetails.titleID)

    time.sleep(int(externalFile.s1configVariables[2]))              # use 'refresh time' variable from external file

# TODO
#  write functions for saving info to external file
#  write function for checking saved info in external file
#  write function to choose between tmdb api images and discord developer application images (gameImage variable will change from link to plaintext)
