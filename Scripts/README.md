## Scripts

These are executable bash scripts for continuous monitoring of incoming files in their
respective folders.

* `bslChecker.sh` : used for uploading `.ihex` files on __Z1__. It is kept in the `/home/pi/bsl` folder

* `incomingChecker.sh` : this keeps a check on incoming data from Back-Channel. This file triggers the 
`configuration.py` script for extracting important information from the `.tar` file. It is kept in the
`/home/pi/incoming` folder

* `createSession.sh` : this script is used as create a detachable `tmux` session at Reboot of the Pi. This file is placed in `/home/pi/bin/` folder.

### Session on Reboot

Place `bin/createSession.sh` in `crontab`:

	nano crontab -e

	## In the crontab file add:

	@reboot /home/pi/bin/createSession.sh

## TMUX Quick Help

Since all the scripts are detached they will not be visible upon a login on a Pi. In order to
attach to these Scripts, use the following:

1. __SSH__ into the Pi:

		ssh -l pi fe80::IPv6:LL:ADDR%wlan0

2. Attach to the created Session:

		tmux a

3. The first window will be a blank shell. According to `createSession`:
	* `TWIN.py` is running at __window:1__
	* `incomingChecker` is running at __window:2__
	* `bslChecker` is running at __window:3__

	To connect to any of the above mentioned windows use the following key combos:

	<kbd>CTRL</kbd>+<kbd>B</kbd>+<kbd>1</kbd>

	or

	<kbd>CTRL</kbd>+<kbd>B</kbd>+<kbd>2</kbd>

	or

	<kbd>CTRL</kbd>+<kbd>B</kbd>+<kbd>3</kbd>

	You can view outputs of the Scripts.

4. Once your work is done, go back to __detached mode__ using :

	<kbd>CTRL</kbd>+<kbd>B</kbd>+<kbd>D</kbd>

5. If you want to kill the complete session:
	
		tmux kill-session