# PS3-Rich-Presence-for-Discord
 
Discord Rich Presence application for PlayStation 3 written in Python.
## Features
* Automatically find PS3 IP address (slow)
* Display name and individual game cover of currently open PS3 game
* Display PS3 temperature and fan speed
* Display name and a single cover for currently open PS2 and PS1 game
 
## Examples
 No game 	| 	PS3 game 	|	PS2 game 	|	PS1 game 	|
 -----------|---------------|---------------|---------------|
 ![noGame](https://imgur.com/gdAaT1F.png) | ![ps3Game](https://imgur.com/ZD1BF70.png) | ![ps2Game](https://imgur.com/n7o0msJ.png) | ![ps1Game](https://imgur.com/CYlTcm6.png)
 
## Usage

### Requirements
* PS3 with webmanMOD installed (program is written working with v1.47.35)
* PS3 and PC on the same network/internet connection

### Installation
A compiled .exe file is provided for use on the windows platform. 
Full discretion: This file is flagged as a virus on my computer, i do not know what causes the file to be flagged.

Alternatively the PS3RPD.py file can be put into your favourite python IDE and ran from there. (Note the required dependencies listed at the bottom of this readme file)

### General instructions
When running the program, the user will be prompted for how the program should get the PS3's ip address, either manually or automatically.
If manual option is chosen, user can enter PS3's IP address.
If automatic option is chosen, program will get the PC's IP address and use this to attempt to find the PS3's.

* NOTE: Due to the way webman works when running PS2 games, the program __will not__ update the RPC, it will instead "freeze" (not heavily tested)

the "implementedImage.txt" file is not required, however without it any PS3 game that does not currently have art assets will display no image at all,
please place this file in the same directory as the .py/.exe file you are running the program from

## Contact me
if you have any PS3 games you wish to have cover art implemented into the program, or any other enquiries for that matter, please contact me via discord: "zorua98741#0023".
Please message me the output next to "validate():" as that will be the name of the art asset added. 

## Remote Python packages required
* urllib3
* BeautifulSoup4
* PyPresence
* requests

## TODO
* implement ability to change time between updates to RPC (currently set to 2 minutes)
* implement more PS3 game covers
* squish bugs
* (eventually) implement GUI to replace CLI