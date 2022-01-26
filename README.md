# PS3-Rich-Presence-for-Discord
Discord Rich Presence script for PS3 consoles on HFW&HEN or CFW.
Written in Python.

Display what you are playing on your PS3 via Discord's game activity.

## Features
* Automatically find PS3 IP address
* Display the name and a game cover for currently open PS3 game
* Display PS3 temperature and fan speed (toggleable)
* Display the name, and either a shared cover, or an individual cover for currently mounted PSX and PS2 game (toggleable)
	- NOTE: PSX and PS2 game detection will **not** work on PSN .pkg versions

## Display Example
 No game 	| 	PS3 game 	|	PS2 game 	|	PS1 game 	|
 -----------|---------------|---------------|---------------|
 ![noGame](https://i.imgur.com/lw1vMGz.png) | ![ps3Game](https://i.imgur.com/aQxcbQG.png) | ![ps2Game](https://i.imgur.com/Z5vYdog.png) | ![ps1Game](https://i.imgur.com/7qfsisz.png) |

## Usage

### Requirements
* PS3 with either HFW&HEN, or CFW installed
* PS3 with [webmanMOD](https://github.com/aldostools/webMAN-MOD/releases) installed (tested working with v1.47.35/36/37)
* PS3 and PC on the same network/internet connection
* Discord installed and open on the PC running the script
* A Python 3.9 interpreter installed on the PC if you do not wish to use the executable file

### Installation
A compiled executable (.exe) is provided for use on the windows platform. 
WARNING: This file was flagged as a virus on my computer, i do not know what causes the file to be flagged as such.

Alternatively, the PS3RPD.py file can be ran from your favourite python IDE. (you will require the external dependencies listed [here](https://github.com/zorua98741/PS3-Rich-Presence-for-Discord#remote-python-packages-required)).  
Note that this script was written with pyton 3.9, i cannot provide support for earlier versions.

### General instructions
On program start, the script will prompt the user for how to get the PS3's IP address.

If the manual option is chosen, the user can enter the PS3's IP address.

If the automatic option is chosen, the program will take the PC's local IP address, and attempt to connect to each address in range 2 - 254.
Each attempt will take ~20 seconds, because of this if your PS3 has an IP address of 192.168.0.200, it will take approximately **1.1 hours** to complete.

Once the script has connected to your PS3, it will generate an external config file, **"PS3RPDconfig.txt"** in the same directory as the script (more information [here](https://github.com/zorua98741/PS3-Rich-Presence-for-Discord#external-config-file)). It will automatically begin sending the game data to your Discord profile.

## Contact Me
please contact me via Discord: "zorua98741#0023".


## Additional Information

### Remote Python packages required
*These are not intended download links, they are the developers sites, please install with pip.*
* [urllib3](https://urllib3.readthedocs.io/en/stable/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [pypresence](https://github.com/qwertyquerty/pypresence)
* [requests](https://docs.python-requests.org/en/latest/)

### External config file
PS3RPD makes use of an external config file to persistently store a few variables, on creation, the default values will be:
* Your PS3's IP address 	(where the script will find your PS3 on the network)
* My Discord developer application's ID 		(where the script will send presence data to)
* A refresh time of 35 seconds 					(how often to get new data (minimum value of 15 seconds)
* To show the PS3's temperature 				(self explanatory)
* To use a shared cover for PS2&PSX games   	(self explanatory) 

You may change these values to suit your own tastes, an example is shown below:

IP | ID | Refresh time(seconds) | Show temperatures | Individual PS2&PSX covers | Output |
---|----|-----------------------|-------------------|---------------------------|--------|
192.168.0.13 | 780389261870235650 | 35 | True | False | ![defaults](https://i.imgur.com/E7M4yie.png) |
192.168.20.5 | 123456789012345678 | 15 | False | True | ![noTemp,indivCover](https://i.imgur.com/QHMxhnj.png) |

Please note that the external config file is sensitive to the data you input, and a change in the formatting **will** most likely break it.

Possible values for the variables:  
* __IP:__ any valid IPv4 address
* __ID:__ any valid Discord developer application ID
* __Refresh time(seconds):__ any digit in range 15-1000 	(Note: any value <15 will be set to 15 due to developer application restraints)
* __Show temperatures:__ [True, true] [False, false]
* __Individual PS2&PSX covers:__ [True, true] [False, false]

### Using your own images
**UPDATE: Rich presence can now display images from an external server, i will be looking into if there is a viable way to do this**  
If you would like to have complete control over what images are used per game, you must create your own Discord developer application over at https://discord.com/developers/applications.

Once created, copy the "APPLICATION ID" from the developer portal and paste it as to replace the current string next to "ID: " in the external config file "PS3RPDconfig.txt".
Alertnatively, if you are using the .py file, you can replace the value of line 26 "self.client_id = ".

You will now be able to add your own art assets in the developer portal under "Rich Presence > Art Assets". Note that the name of the art assets uploaded must be the same as whatever is output from "validate(): " when that specific game is open.

An example:  
If i want to add an image for Counter Strike: Global Offensive, I will open the game and look for the output of "validate():" from the PS3RPD script on my PC:  
![validateExample](https://i.imgur.com/7EEgUYn.png)  
As shown, i would then rename the art asset on my PC "counter_strike_global_offensive_", and upload it to my Discord developer application.

After a couple of minutes, CS:GO will go from having no image, to displaying an art asset from the developer application:  
before | after |
-------|-------|
![noasset](https://i.imgur.com/8mJvYDH.png) | ![addedasset](https://i.imgur.com/XLIsIVV.png) |

### (in)Frequently asked questions
Q: Can this script be adapted for use on mobile devices?  
A: no. While the functionality of this script could certainly be adapted into a mobile app. Discord does not support rich presence from its mobile app.

Q: Can this script be used on OFW/without webmanMOD?  
A: no. The only other program i have encountered that i can scrape game info from is CCAPI, which is lesser-used, and more complicated for the user to setup than webmanMOD.

Q: Why does [insert game name here] not have an image when i play it?  
A: either you have not waited long enough for your art asset to be uploaded into your own developer application, or, you are using my developer application,
where i am limited to adding only the games i can play on my PS3 (that i own), if you would like to use my developer application, but with more images, please [message me on discord](https://github.com/zorua98741/PS3-Rich-Presence-for-Discord#contact-me),
and i will be more than happy to add the game/s for you.

Q: Why is PS2 game detection inconsistent?  
A: this script works by scraping game data from webmanMOD. When a PS3 goes into PS2 mode, it disables all plugins including webmanMOD,
because of this the script will only detect a PS2 game if it refreshes itself and it finds a PS2 game mounted (but not open).  
There is no way of fixing this issue as far as i can tell.

Q: Can i programatically send art assets to Discord?  
~~A: no, Discord does not currently offer the option to do this, 
the only option currently is to upload the art asset to the Discord developer application and use naming conventions to call a specific art asset depending on what game is open~~
A: maybe! I am currently working on a way to do this

Q: I want Discord to show me playing the game's name, not playing "PS3", can i do this?  
A: yes, however to do so each game will require its own Discord developer application, and this specific script is not made to support such a manual task.  
If you **really** require this feature, i can slap together another version of PS3RPD and demonstrate to you how to manually add games, however i will not waste my time doing so if such a branch is not highly requested, and you will be expected to create and add the applications yourself

### Implemented images
Below is a table of all games that have an art asset on **my** Discord developer application, you should be able to save these images and add them to your own developer app if you wish.  
image | name | validated name |
------|------|----------------|
![rebugToolbox](https://cdn.discordapp.com/app-assets/780389261870235650/835783442657837076.png) | Rebug Toolbox | \_rebug_toolbox_ |
![batman](https://cdn.discordapp.com/app-assets/780389261870235650/805248753983815691.png) | Batman Arkham Asylum GOTY | batman_arkham_asylum_goty_ |
![batman2](https://cdn.discordapp.com/app-assets/780389261870235650/805251424131743745.png) | Batman Arkham City GOTY | batman_arkham_city_goty_ |
![batman3](https://cdn.discordapp.com/app-assets/780389261870235650/805261554789908490.png) | Batman Arkham Origins | batman_arkham_origins_ |
![battlefield4](https://cdn.discordapp.com/app-assets/780389261870235650/805269690145570816.png) | Battlefield 4 | battlefield_4_ | 
![battlefieldhardline](https://cdn.discordapp.com/app-assets/780389261870235650/805283861584019506.png) | Battlefield Hardline | battlefield_hardline_ |
![burnoutparadise](https://cdn.discordapp.com/app-assets/780389261870235650/805414048396476436.png) | Burnout Paradise The Ultimate Box | burnout_paradise_the_ultimate_bo |
![COD4](https://cdn.discordapp.com/app-assets/780389261870235650/805415528725479426.png) | COD 4: Modern Warfare | call_of_duty_4_modern_warfare_ |
![CODAW](https://cdn.discordapp.com/app-assets/780389261870235650/805094734863401010.png) | COD: Advanced Warfare | call_of_duty_advanced_warfare_ |
![CODBO1](https://cdn.discordapp.com/app-assets/780389261870235650/805417116256960533.png) | COD: Black Ops | call_of_duty_black_ops_ |
![CODBO2](https://cdn.discordapp.com/app-assets/780389261870235650/805417924549804043.png) | COD: Black Ops 2 | call_of_duty_black_ops_ii_ |
![CODG](https://cdn.discordapp.com/app-assets/780389261870235650/805418541896957952.png) | COD: Ghosts | call_of_duty_ghosts_ |
![CODMW3](https://cdn.discordapp.com/app-assets/780389261870235650/805420360232075284.png) | COD: MW3 | call_of_duty_modern_warfare_3_ |
![catherine](https://cdn.discordapp.com/app-assets/780389261870235650/816819805612933120.png) | Catherine | catherine_ |
![CSGO](https://cdn.discordapp.com/app-assets/780389261870235650/909654118480642059.png) | CSGO | counter_strike_global_offensive_ |
![DS2](https://cdn.discordapp.com/app-assets/780389261870235650/805602703765274644.png) | Dark Souls 2 scholar of the first sin | dark_souls_ii_scholar_of_the_fir |
![DS1](https://cdn.discordapp.com/app-assets/780389261870235650/805604622823194686.png) | Dark Souls prepare to die edition | dark_souls_prepare_to_die_editio |
![deadpool](https://cdn.discordapp.com/app-assets/780389261870235650/805604645916639232.png) | Deadpool | deadpool_ |
![DAI](https://cdn.discordapp.com/app-assets/780389261870235650/805619836633612288.png) | Dragon Age Inquisition | dragon_age_inquisition_ |
![FC3](https://cdn.discordapp.com/app-assets/780389261870235650/805631524069572619.png) | Far Cry 3 | far_cry_3_ |
![FFXIII](https://cdn.discordapp.com/app-assets/780389261870235650/810357869417201679.png) | Final Fantasy XIII | final_fantasy_xiii__ |
![FFXIII2](https://cdn.discordapp.com/app-assets/780389261870235650/808244624303980574.png) | Final Fantasy XIII-2 | final_fantasy_xiii-2_ |
![FFXX-2](https://cdn.discordapp.com/app-assets/780389261870235650/809233149287858176.png) | Final Fantasy XX-2 HD remaster | final_fantasy_xx-2_hd_remaster_ |
![GOWcollection](https://cdn.discordapp.com/app-assets/780389261870235650/808545777219665942.png) | God of War collection | god_of_war_collection_ |
![GOWcollection2](https://cdn.discordapp.com/app-assets/780389261870235650/808241113735233546.png) | God of War collection volume II | god_of_war_collection_volume_ii_ |
![GOW3](https://cdn.discordapp.com/app-assets/780389261870235650/808239694814117918.png) | God of War III | god_or_war_iii_ |
![GT6](https://cdn.discordapp.com/app-assets/780389261870235650/815481412400578600.png) | Gran Turismo 6 | gran_turismo6_ |
![icoshadow](https://cdn.discordapp.com/app-assets/780389261870235650/808236434699976705.png) | Ico & Shadow of the colossus collection | ico__shadow_of_the_colossus_clas |
![infamous1](https://cdn.discordapp.com/app-assets/780389261870235650/806789600122634251.png) | Infamous | infamous_ | 
![infamous2](https://cdn.discordapp.com/app-assets/780389261870235650/806788653871005716.png) | Infamous 2 | infamous_2_ | 
![jakdaxter](https://cdn.discordapp.com/app-assets/780389261870235650/806350951774421084.png) | Jak and Daxter collection | jak_and_daxter_collection_ |
![Jojo](https://cdn.discordapp.com/app-assets/780389261870235650/891952659517558804.png) | JoJos bizarre adventure all-star battle | jojos_bizarre_adventure_all-star |
![KH15](https://cdn.discordapp.com/app-assets/780389261870235650/816572987662270494.png) | Kingdom Hearts HD 1.5 remix | kingdom_hearts_hd_15_remix_ |
![KH25](https://cdn.discordapp.com/app-assets/780389261870235650/816622915009249280.png) | Kingdom Hearts HD 2.5 remix | kingdom_hearts_hd_25_remix_ |
![MGS4](https://cdn.discordapp.com/app-assets/780389261870235650/846676900729585704.png) | Metal Gear Solid 4 guns of the patriots | metal_gear_solid_4_guns_of_the_p |
![MGScollection](https://cdn.discordapp.com/app-assets/780389261870235650/806778256459038771.png) | Metal Gear Solid HD collection | metal_gear_solid_hd_collection_ |
![MGS5GZ](https://cdn.discordapp.com/app-assets/780389261870235650/806786268352086036.png) | Metal Gear Solid V Ground Zeroes | metal_gear_solid_v_ground_zeroes
![mmcm](https://cdn.discordapp.com/app-assets/780389261870235650/835053825978400818.png) | Multiman | mmcm_ |
![CODMW2](https://cdn.discordapp.com/app-assets/780389261870235650/805419331286335548.png) | COD: Modern Warfare 2 | modern_warfare_2_ |
![NFSHP](https://cdn.discordapp.com/app-assets/780389261870235650/806773086568710164.png) | Need for Speed Hot Pursuit | need_for_speed_hot_pursuit_ |
![NFSMW](https://cdn.discordapp.com/app-assets/780389261870235650/806772516307337247.png) | Need for Speed Most Wanted | need_for_speed_most_wanted_ |
![NFSR](https://cdn.discordapp.com/app-assets/780389261870235650/806769551013707826.png) | Need for Speed Rivals | need_for_speed_rivals_ |
![OOA](https://cdn.discordapp.com/app-assets/780389261870235650/928285998180352063.png) | OutRun Online Arcade | outrun_online_arcade_ |
![P4AU](https://cdn.discordapp.com/app-assets/780389261870235650/805669120829292576.png) | Persona 4 Arena Ultimax | persona_4_arena_ultimax_ |
![P5](https://cdn.discordapp.com/app-assets/780389261870235650/808652126443929601.png) | Persona 5 | persona_5_ | 
![RCa4o](https://cdn.discordapp.com/app-assets/780389261870235650/805666595249717248.png) | Ratchet & Clank all 4 one | ratchet__clank_all_4_one_ |
![RCffa](https://cdn.discordapp.com/app-assets/780389261870235650/805663243103502346.png) | Ratchet & Clank full frontal assault | ratchet__clank_full_frontal_assa |
![RCfacit](https://cdn.discordapp.com/app-assets/780389261870235650/805657865452650496.png) | Ratchet & Clank future a crack in time | ratchet__clank_future_a_crack_in |
![RCn](https://cdn.discordapp.com/app-assets/780389261870235650/805648727842750474.png) | Ratchet & Clank nexus | ratchet__clank_nexus_ |
![RCqfb](https://cdn.discordapp.com/app-assets/780389261870235650/805650458164330496.png) | Ratchet & Clank quest for booty | ratchet__clank_quest_for_booty_ |
![RCtod](https://cdn.discordapp.com/app-assets/780389261870235650/805661114452803624.png) | Ratchet & Clank tools of destruction | ratchet__clank_tools_of_destruct |
![RDR](https://cdn.discordapp.com/app-assets/780389261870235650/805078088639578122.png) | Red Dead Redemption GOTY | red_dead_redemption_game_of_the_ |
![skate](https://cdn.discordapp.com/app-assets/780389261870235650/919957926087622706.png) | Skate | skate_ |
![skate2](https://cdn.discordapp.com/app-assets/780389261870235650/919957590060982273.png) | Skate 2 | skate_2_ |
![skate3](https://cdn.discordapp.com/app-assets/780389261870235650/919961868490125342.png) | Skate 3 | skate_3_ |
![RCt](https://cdn.discordapp.com/app-assets/780389261870235650/805645315373924394.png) | The Ratchet & Clank Trilogy | the_ratchet__clank_trilogy_ |
![simpsons](https://cdn.discordapp.com/app-assets/780389261870235650/805639154191958046.png) | The Simpsons Game | the_simpsons_game_ |
![ps2](https://cdn.discordapp.com/app-assets/780389261870235650/835176560746168360.png) | PS2 | ps2 |
![psx](https://cdn.discordapp.com/app-assets/780389261870235650/835176545102463016.png) | PS1 | psx |
![ps3rpd](https://cdn.discordapp.com/app-assets/780389261870235650/835176477653073940.png) | PS3RPD logo | xmb |