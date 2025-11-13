# PS3-Rich-Presence-for-Discord
Discord Rich Presence script for PS3 consoles on HFW&HEN or CFW.

Display what game you are playing on PS3 via your PC!

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
		<th> <img src="https://github.com/zorua98741/PS3-Rich-Presence-for-Discord/blob/main/img/retro.png?raw=true"> </th>
	</tr>
</table>


## Usage

### Requirements
* PS3 with either HFW&HEN, or CFW installed
* PS3 with [webmanMOD](https://github.com/aldostools/webMAN-MOD/releases) installed 
* PS3 and PC on the same network/internet connection
* Discord installed and open on the PC running the script
* Administrator permissions on the PC
* A Python 3.9 interpreter installed on the PC if you do not wish to use the executable file

### Windows
* ~~[version 1.9.7 .exe](https://github.com/zorua98741/PS3-Rich-Presence-for-Discord/releases/download/v1.9.7/PS3RPD.exe)~~
or
* [version 1.9.7 .py](https://github.com/zorua98741/PS3-Rich-Presence-for-Discord/releases/download/v1.9.7/PS3RPD.py)

#### Installing as a Windows service (optional)
Download [NSSM](https://nssm.cc/release/nssm-2.24.zip) and run `nssm install <service name ie. ps3rpd>` to install PS3RPD as a Windows service.
WARNING: PS3RPD.exe must be in a location that won't change ie. C:\ps3rpd\PS3RPD.exe

> [!NOTE]
> The executable file will very likely be flagged as a virus on your computer due to `pyinstaller` being used to compile it.
> As far as I know, there is nothing I can do to fix this.

### Linux 

To download and run the script for the first time:
```bash
# Clone the GitHub repository under the user folder
git clone https://github.com/zorua98741/PS3-Rich-Presence-for-Discord ~/ps3-rich-presence
# Run the start script
cd ~/ps3-rich-presence && ./start.py
```

From there you can run the script via double clicking on the file within your file explorer, and clicking on "Run (in terminal)".<br>
Alternatively, you can run the command via the terminal by running `cd ~/ps3-rich-presence && ./start.py` again.

#### Installing as a systemd service (optional)
<details>
  <summary>If you would like the script to start on device boot, after the first run, run the following commands in your terminal:</summary>
<br>
	
```bash
# Creates the user service folder if it doesn't exist yet, and the user systemd env folder
mkdir -p ~/.config/systemd/user ~/.config/environment.d/
# Include local binaries in your systemd user environment
# (we need this so systemd can find the 'uv' executable)
bash -c 'echo "
# Adds ~/.local/bin to PATH so systemd services can find user-installed binaries
PATH=${HOME}/.local/bin:
" >> ~/.config/environment.d/90-path.conf'

# Creates a systemd .service file in the user service folder that runs the script
bash -c 'echo "
[Unit]
Description=Enables Discord Rich Presence for PS3
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/usr/bin/python3 $HOME/ps3-rich-presence/start.py
Restart=on-failure
StandardOutput=journal
StandardError=journal
WorkingDirectory=$HOME/ps3-rich-presence

[Install]
WantedBy=default.target
" > ~/.config/systemd/user/ps3rpd.service'
# Reloads the systemd service to recognize the new service
systemctl --user daemon-reload
# Enables the service and starts it
systemctl --user enable --now ps3rpd
# Make it clear that something happened
echo "Finished adding user service for ps3rpd."
echo "You can check the status of the service with `systemctl --user status ps3rpd`"
```

In order to check the health of the service, you can run `systemctl --user status ps3rpd`<br>
For more depth logs you can use `journalctl --user -xeu ps3rpd`
</details>

## Limitations
* __A PC must be used to display presence, there is no way to install and use this script solely on the PS3__
* The script relies on webmanMOD, and a major change to it will break this script, please message me about updated versions of webman so that i can test the script with them
* PSX and PS2 game name depends on the name of the file
* PSX and PS2 game detection will **not** work on PSN .pkg versions because webman cannot show those games as mounted/playing.
* PS2 ISO game detection can be inconsistent, varying on degree of consistency by the value of "Refresh time."
* Using Windows 7 is only possible with up to PS3RPD version 1.7.2
	- If you want to use a .exe, [here](https://www.mediafire.com/file/ezzlcemhkmnmyn2/PS3RPD.exe/file) is a version that may or may not fully function (very little bug testing has been done)

## Contact Me
Contact me via Discord: `zorua98741`/`zorua98741#0023`.

## Additional Information

### External config file
PS3RPD makes use of an external config file to persistently store a few variables, on creation, the default values will be:
* Your PS3's IP address 	(where the script will find your PS3 on the network)
* My Discord developer application's ID 		(where the script will send presence data to)
* A refresh time of 35 seconds 					(how often to get new data (minimum value of 15 seconds)
* To show the PS3's temperature
* To use a shared cover for PS2&PSX games
* To display the time elapsed

### Using your own images
If you'd like to control what images are used for each game, you must create a Discord Developer Application over at the [Discord Developer Portal](https://discord.com/developers/applications).

Once created, copy the application ID from the Developer Portal and paste it into the external `ps3rpdconfig.json`, replacing the value of `client_id`.

You are now able to upload your own assets in the Developer Portal under `Rich Presence > Art Assets`. Note that the name of the asset uploaded must be the lowercase title ID provided in the script's output. (e.g. `abcd12345`)

## [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N87V7K5) [![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
