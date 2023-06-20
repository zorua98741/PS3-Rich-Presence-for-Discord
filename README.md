# PS3-Rich-Presence-for-Discord
Discord Rich Presence script for PS3 consoles on HFW&HEN or CFW.

Display what you are playing on your PS3 via Discord's game activity.

## Display Example
<table>
	<tr>
		<th>XMB</th>
		<th> <img src="https://github.com/zorua98741/PS3-Rich-Presence-for-Discord/blob/main/img/xmb.png?raw=true"> </th>
	</tr>
	<tr>
		<th>PS3</th>
		<th> <img src="https://github.com/zorua98741/PS3-Rich-Presence-for-Discord/blob/main/img/ps3.png?raw=true"> </th>
	</tr>
	<tr>
		<th>Retro</th>
		<th> <img src="https://github.com/zorua98741/PS3-Rich-Presence-for-Discord/blob/main/img/xmb.png?raw=true"> </th>
	</tr>
</table>
## Limitations
* __A PC must be used to display presence, there is no way to install and use this script solely on the PS3__
* PSX and PS2 game detection depends on the name of the file
* PSX and PS2 game detection will **not** work on PSN .pkg versions because webman cannot show those games as mounted/playing.
* PS2 ISO game detection can be inconsistent, varying on degree of consistency by the value of "Refresh time."
* Using Windows 7 is only possible with up to PS3RPD version 1.7.2
	- If you want to use a .exe, [here](https://www.mediafire.com/file/ezzlcemhkmnmyn2/PS3RPD.exe/file) is a version that may or may not fully function (very little bug testing has been done)
* The script relies on webmanMOD, and a major change to it will break this script, please message me about updated versions of webman so that i can test the script with them

## Usage

### Requirements
* PS3 with either HFW&HEN, or CFW installed
* PS3 with [webmanMOD](https://github.com/aldostools/webMAN-MOD/releases) installed 
* PS3 and PC on the same network/internet connection
* Discord installed and open on the PC running the script
* A Python 3.9 interpreter installed on the PC if you do not wish to use the executable file

### Installation
A compiled executable (.exe) is provided for use on the windows platform.  
WARNING: This file will likely be flagged as a virus on your computer due to pyinstaller.

Alternatively, the PS3RPD.py file can be ran from your favourite python IDE.
Note that this script was written with python 3.9, i cannot guarantee support for earlier or later versions.

### Installing as a Windows service (optional)
Download [NSSM](nssm.cc/release/nssm-2.24.zip) and run `nssm install <service name ie. ps3rpd>` to install PS3RPD as a Windows service.
WARNING: PS3RPD.exe must be in a location that won't change ie. C:\ps3rpd\PS3RPD.exe

## Contact Me
please contact me via Discord: "zorua98741#0023"/"zorua98741".

## Additional Information

### External config file
PS3RPD makes use of an external config file to persistently store a few variables, on creation, the default values will be:
* Your PS3's IP address 	(where the script will find your PS3 on the network)
* My Discord developer application's ID 		(where the script will send presence data to)
* A refresh time of 35 seconds 					(how often to get new data (minimum value of 15 seconds)
* To show the PS3's temperature 				(self explanatory)
* To use a shared cover for PS2&PSX games   	(self explanatory) 
* To reset the *time elapsed* whenever a new game is opened

Possible values for the variables:  
* __IP:__ any valid IPv4 address
* __ID:__ any valid Discord developer application ID
* __Refresh time(seconds):__ any digit in range 15-1000 	(Note: any value <15 will be set to 15 due to developer application restraints)
* __Show temperatures:__ [True, true] [False, false]
* __Individual PS2&PSX covers:__ [True, true] [False, false]
* __Reset time elapsed on game change:__ [True, true] [False, false]


### Using your own images
If you would like to have complete control over what images are used per game, you must create your own Discord developer application over at https://discord.com/developers/applications.

Once created, copy the "APPLICATION ID" from the developer portal and paste it as to replace the current string next to "ID: " in the external config file "PS3RPDconfig.txt".
Alertnatively, if you are using the .py file, you can replace the value of "self.client_id".

You will now be able to add your own art assets in the developer portal under "Rich Presence > Art Assets". Note that the name of the art assets uploaded must be the same as whatever is output from "validate(): " when that specific game is open.

An example:  
If i want to add an image for Counter Strike: Global Offensive, I will open the game and look for the output of "validate():" from the PS3RPD script on my PC:  
![validateExample](https://i.imgur.com/7EEgUYn.png)  
As shown, i would then rename the art asset on my PC "counter_strike_global_offensive_", and upload it to my Discord developer application.

After a couple of minutes, CS:GO will go from having no image, to displaying an art asset from the developer application:
before | after |
-------|-------|
![noasset](https://i.imgur.com/8mJvYDH.png) | ![addedasset](https://i.imgur.com/XLIsIVV.png) |

## [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N87V7K5) [![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
