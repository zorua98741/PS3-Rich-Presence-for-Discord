# Need to test if urllib3 causes PS3 to crash less often!

from socket import socket, AF_INET, SOCK_DGRAM  # used to get host IP address
import re  # used for regular expressions
import networkscan  # used for automatic obtaining IP address, requires pip install
import os  # used to test if config exists
import requests  # used to test if given IP belongs to PS3, requires pip install
from requests.exceptions import ConnectionError  # used to handle thrown errors on connecting to webpage
from bs4 import BeautifulSoup   # used for webpage scraping, requires pip install
from time import sleep          # used to add delay to mitigate rate limiting and webmanMOD memory consumption
# from pypresence import Presence, InvalidPipe, InvalidID     # pypresence requires pip install


class PrepWork:     # Python2 class should be "class PrepWork(object):" ?
    def __init__(self):
        self.ip = None
        self.clientID = '780389261870235650'
        self.waitTime = '35'  # seconds
        self.showTemps = 'True'
        self.indivRetroCovers = 'False'
        self.resetTimer = 'False'

    def read_config(self):
        if os.path.isfile('PS3RPDconfig.txt'):  # test if file exists
            file = open('PS3RPDconfig.txt', 'r')
            lines = file.readlines()
            try:    # overwrite default values with values stored in config file
                # ! regex could be improved !
                self.ip = re.search('([0-9]{1}.*)', lines[0]).group(1)  # capture start at 1 or more number to end of string
                self.clientID = re.search(': (.*)', lines[1]).group(1)  # capture start after ": " to end of string
                self.waitTime = re.search(': (.*)', lines[2]).group(1)
                if int(self.waitTime) < 15:     # waitTime is limited by Discord, do not allow it to be less than 15
                    self.waitTime = "15"
                self.showTemps = re.search(': (.*)', lines[3]).group(1)
                self.indivRetroCovers = re.search(': (.*)', lines[4]).group(1)
                self.resetTimer = re.search(': (.*)', lines[5]).group(1)
            except Exception as e:
                exit(f'error with config file "{e}". \nTry deleting it or contact the developer.')
            if self.test_for_webman(self.ip):    # IP in config still belongs to PS3
                pass    # ! connect and begin gathering details from webman here !
            else:   # IP in config does not belong to PS3
                print('IP in config file is not detected as belonging to a PS3, please check if it has changed.')
                self.promptUser()
        else:   # file does not exist
            print('no config found!')
            self.promptUser()

    def promptUser(self):
        choice = 'placeholder'
        accepted = ['a', 'm']
        print("Get PS3's IP address automatically, or manually?")
        while choice[0].lower() not in accepted:  # test if first character of choice is in array
            choice = input('Please enter either "A", or "M": ')
        if choice[0].lower() == 'a':
            self.grab_host_network()
        elif choice[0].lower() == 'm':
            self.get_IP_from_user()
        else:
            exit('Unexpected input')

    def grab_host_network(self):  # hard to account for what users firewall and network will look like. Function may not work for all users.
        hostNetwork = None
        try:
            tempSock = socket(AF_INET, SOCK_DGRAM)
            tempSock.connect(('8.8.8.8', 80))
            hostNetwork = tempSock.getsockname()[0]
            tempSock.close()
        except Exception as e:
            print(f'Error while getting host network. "{e}"')

        if hostNetwork is not None:
            hostNetwork = re.search('^(.*)\.', hostNetwork).group(0)  # remove machine's octet
            print(f'expected network is "{hostNetwork}"')
            self.scan_network(hostNetwork)

    def scan_network(self, my_network):  # takes IPv4 address in form 'x.x.x.'
        # adapted from nychron's code
        my_network += '0/24'  # append 4th octet and short-form subnet mask
        my_scan = networkscan.Networkscan(my_network)

        # Run the scan of hosts using pings
        my_scan.run()

        # Display the IP address of all the hosts found
        print('Completed network scan.')
        print(my_scan.list_of_hosts_found)

        for i in range(len(my_scan.list_of_hosts_found)):
            if self.test_for_webman(my_scan.list_of_hosts_found[i]):
                self.save_config(my_scan.list_of_hosts_found[i])
                # ! connect and begin gathering details from webman here !
                break   # do not test further IPs if one is found to belong to webman
        # ! NEED TO HANDLE IF PS3 IS NOT FOUND !

    def get_IP_from_user(self):
        while True:
            ip = input("Enter PS3's IP address: ")
            if self.test_for_webman(ip):
                self.save_config(ip)
                # ! connect and begin gathering details from webman here !
                break

    def test_for_webman(self, ip):
        response = None
        url = f'http://{ip}'
        try:    # test if ANY webpage is running on given IP
            response = requests.get(url, headers=headers)
        except ConnectionError as e:
            print(f'No webpage found on "{ip}"')
            return False
        if response is not None:
            soup = BeautifulSoup(response.text, 'html.parser')
            pageTitle = str(soup.find('title'))     # default type is bs4.element.tag, needs to be string
            if 'wMAN' in pageTitle or 'webMAN' in pageTitle:    # test for known value in <title>
                print(f'given IP "{ip}" belongs to webman.')
                return True
            else:   # a webpage was found, but does not satisfy check to belong to webman
                print(f'WebmanMOD not found on "{ip}", reports "{pageTitle}". If you believe this is an error, please contact the developer. '
                      f'Please ensure the PS3 is turned on, has webmanMOD installed and running, '
                      f'and is connected to the same network as the PC.')
                return False

    def save_config(self, validatedIP):     # updates/creates the external config file
        print("Updating/Creating config with saved values")
        self.ip = validatedIP   # update value of variable used in other class
        file = open('PS3RPDconfig.txt', 'w+')   # w+ creates file if it doesn't exist, overwriting previous content
        file.write(f'IP: {self.ip}\n')
        file.write(f'clientID: {self.clientID}\n')  # use config file values if it exists, otherwise default values
        file.write(f'wait time: {self.waitTime}\n')
        file.write(f'show temperature: {self.showTemps}\n')
        file.write(f'use individual art for retro games: {self.indivRetroCovers}\n')
        file.write(f'reset time elapsed on new game: {self.resetTimer}\n')


class GatherDetails:
    def __init__(self):
        self.soup = None
        self.thermalData = None

    def ping_PS3(self):     # Will work if webman is unloaded for some reason, will hopefully greatly reduce risk of
        # PS3 crashing when webman is contacted while also loading or quitting out of a game. (! Needs further testing !)
        os.system(f'ping {prepWork.ip}')

    def get_html(self):
        url = f'http://{prepWork.ip}/cpursx.ps3?/sman.ps3'
        try:
            response = requests.get(url, headers=headers)
            self.soup = BeautifulSoup(response.text, 'html.parser')
            return True
        except ConnectionError as e:
            print(f'get_html():  webman not found. "{e}".')
            return False

    def get_thermals(self):
        thermalData = str(self.soup.find("a", href="/cpursx.ps3?up"))
        # you can change to Fahrenheit by changing "C" to "F".
        cpu = re.search('CPU(.+?)C', thermalData)
        rsx = re.search('RSX(.+?)C', thermalData)
        try:
            cpu = cpu.group(0)
            rsx = rsx.group(0)
            self.thermalData = f'{cpu} | {rsx}'
            print(f'get_thermals():     {self.thermalData}')
        except AttributeError:
            print(f'get_thermals(): could not find html for thermal data, has webmanMOD been updated since {wmanVer}?')

    def decide_game_type(self):
        # PS3 games will only be detected when they are OPEN, however PS2 and PS1 games will be detected when they are MOUNTED
        if self.soup.find('a', target='_blank') is not None:    # PS3ISO, JB Folder Format, and PS3 PKG games will display this field in wman
            print('decide_game_type():  PS3 Game or Homebrew')
            self.get_PS3_details()
        elif self.soup.find('a', href=re.compile('/(dev_hdd0|dev_usb00[0-9])/(PSXISO|PS2ISO)')) is not None:  # search for PSX or PS2 mounted game
            print('decide_game_type():  Retro')
            self.get_retro_details()
        else:
            print('decide_game_type():  XMB')

    def get_PS3_details(self):
        titleID = self.soup.find('a', target='_blank')  # get titleID of open game/homebrew
        name = self.soup.find('a', target='_blank').find_next_sibling()  # get name of open game/homebrew
        try:
            titleID = re.search('>(.*)<', str(titleID)).group(1)     # remove surrounding HTML
            name = re.search('>(.*)<', str(name)).group(1)
            if re.search('(.+)[0-9]{2}.[0-9]{2}', name) is not None:    # remove game version info if present
                name = re.search('(.+)[0-9]{2}.[0-9]{2}', name).group(1)
        except AttributeError:
            print(f'get_PS3_details(): could not find html for game data, has webmanMOD been updated since {wmanVer}?')
        print(f'get_PS3_details():  {titleID} | {name}')

    def get_retro_details(self):    # only tested with PSX and PS2 games, PSP and retroarch game compatibility unknown
        name = 'Retro'  # if a PSX or PS2 game is not detected, this default will be used
        # name detected is based on name of file
        if self.soup.find('a', href=re.compile('/(dev_hdd0|dev_usb00[0-9])/PSXISO')) is not None:   # only PSX
            name = self.soup.find('a', href=re.compile('/(dev_hdd0|dev_usb00[0-9])/PSXISO')).find_next_sibling()
        elif self.soup.find('a', href=re.compile('/(dev_hdd0|dev_usb00[0-9])/PS2ISO')) is not None: # only PS2
            name = self.soup.find('a', href=re.compile('/(dev_hdd0|dev_usb00[0-9])/PS2ISO')).find_next_sibling()
        try:
            name = re.search('\">(.*)</a>', str(name)).group(1)
        except AttributeError as e:
            print(f'! get_retro_details(): error with regex "{e}" !')
        print(f'get_retro_details(): {name}')

    def get_image(self):
        pass


headers = {'Content-Type': 'text/html'}  # Alternatively {"User-Agent": "Mozilla/5.0"}. Used by both classes
wmanVer = '1.47.45'     # static string so I can indicate what ver the script was last tested with

prepWork = PrepWork()
prepWork.read_config()
gatherDetails = GatherDetails()

if prepWork.ip is None:     # very basic error notification for if prepWork breaks
    exit('script failed to load or find IP address.')
while True:
    if not gatherDetails.get_html():    # triggered if webman goes down
        print(f'Webman server not found, waiting {prepWork.waitTime} seconds.')
        sleep(float(prepWork.waitTime))
    else:   # continue with normal program loop
        gatherDetails.get_thermals()
        gatherDetails.decide_game_type()

        print('')
        sleep(float(prepWork.waitTime))
