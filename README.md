# PS3-Rich-Presence-for-Discord
 
Discord Rich Presence application for PlayStation 3 written in Python.
## Features
* Automatically find PS3 IP address (slow)
* Display name and individual game cover of currently open PS3 game
* Display PS3 temperature and fan speed
* Display name and a single cover for currently open PS2 and PS1 game
 
## Examples
<!-- ### Old layout
 No game 	| 	PS3 game 	|	PS2 game 	|	PS1 game 	|
 -----------|---------------|---------------|---------------|
 ![noGame](https://imgur.com/gdAaT1F.png) | ![ps3Game](https://imgur.com/ZD1BF70.png) | ![ps2Game](https://imgur.com/n7o0msJ.png) | ![ps1Game](https://imgur.com/CYlTcm6.png)
-->
### New layout
 No game 	| 	PS3 game 	|	PS2 game 	|	PS1 game 	|
 -----------|---------------|---------------|---------------|
 ![noGame](https://i.imgur.com/lw1vMGz.png) | ![ps3Game](https://i.imgur.com/aQxcbQG.png) | ![ps2Game](https://i.imgur.com/Z5vYdog.png) | ![ps1Game](https://i.imgur.com/7qfsisz.png) |
 
## Usage

### Requirements
* PS3 with webmanMOD installed (program is written working with v1.47.35)

* PS3 and PC on the same network/internet connection

### Installation
A compiled .exe file is provided for use on the windows platform. 
Full discretion: This file is flagged as a virus on my computer, i do not know what causes the file to be flagged.

Alternatively the PS3RPD.py file can be put into your favourite python IDE and ran from there. (Note the required external dependencies listed at the bottom of this readme file)

### General instructions
On program start, user will be prompted for how the program should get the PS3's ip address <br>
If manual is chosen, user can enter PS3's IP address. <br>
If automatic is chosen, program will find the PS3's IP address. <br>
Each IP address will be tested for 20 seconds, if your PS3 has an IP address of 192.168.0.200, it will take approx 1.1 hours to complete, due to this it is recommended to manually enter the IP. <br>

* NOTE: Due to the way webman works when running PS2 games, the program __will not__ update the RPC, it will instead "freeze" (This function has not been tested and will likely have bugs)

the "implementedImage.txt" file is not required, however without it any PS3 game that does not currently have art assets will display no image at all,
please place this file in the same directory as the .py/.exe file you are running the program from

 Without .txt file 	| With .txt file |
 -------------------|----------------|
 ![notxtfile](https://imgur.com/xrkHBgC.png) | ![txtfile](https://imgur.com/LQKekql.png)

## Contact me
please contact me via discord: "zorua98741#0023". <br>
If you would like me to add game art to my developer application for your use, please message me the output of "validate():" for the game/s

## Remote Python packages required
* urllib3
* BeautifulSoup4
* PyPresence
* requests

## Using your own images
If you would like to have complete control over what images are used per game, you must create your own Discord developer application over at https://discord.com/developers/applications. <br>
Once created, copy the "APPLICATION ID" from the developer portal and replace the value of the variable "client_id" inside the python file. **there is currently no way to use your own images with the compiled .exe file**. <br>
You will now be able to add your own art assets in the developer portal under "Rich Presence > Art Assets". Note that there are naming conventions you will have to follow, and thus you will name the image/art asset the output of "validate():" <br>
 ![example](https://imgur.com/QUZ6GTq.png) <br>
Note how the game's name is different to "validate()", and that to add an image for CSGO, the art asset in the Discord developer application would be named "counter_strike_global_offensive_".
Finally, for the names of the art assets to be sent to *your* discord developer application, you have the option of either deleting "implementedImage.txt" or otherwise deleting all current text in the file, and adding your own names.

## (un)Frequently Asked Questions
Q: Can this script be adapted for use on mobile devices? <br>
A: no. While the functionality of this script could easily be adapted into a mobile app, Discord does not widely support rich presence from its mobile app. If this changes please notify me and i'll (probably) start work on it.

Q: Can this script be used without webmanMOD? <br>
A: no. The only other program i have encountered that i can scrape active game info from is CCAPI, which is lesser-used, and more complicated for the user to set-up than webmanMOD.

Q: Do i need to use the implementedImage.txt? <br>
A: no, and i will be working on a way to remove it entirely.

## TODO
* implement ability to change time between updates to RPC (currently set to 35 seconds)
* implement ability to disable temps & fan-speed display,
* implement ability to change Discord Developer Application without changing variables (for .exe version),
* find a way to remove need for implementedImage.txt?,
* rewrite this README.md so its less of a word soup, and is easier to understand
* rework PS2 presence detection to work more often
* implement more PS3 game covers!!
