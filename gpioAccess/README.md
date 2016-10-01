# GPIO Access using HTTP

Since all the TWIN Nodes use the __IPv6 Link-Local Address__,
current web-browsers do not support the addressing scheme. However,
a command-line utility over __HTTP__ is developed here.

## Dependency

All GPIO pin access is done via creating __Flask__. Use the following
to install Flask on the Pi:

	sudo pip install flask

__Note__: flask is developed for __Python2__ and hence use `pip`

### Running the Script

add the following line in `~/bin/createSession.sh`

	/usr/bin/tmux new-window -d -n 'GPIOaccess' -t TWIN:4 'sudo ~/gpioAccess/gpioAPI.py'

one needs the superuser access for __Flask__ applications.


## API for GPIO Access

Since webbrowser access in not available for Link-Local Addresses we use `curl` on command-line
as follows:

	curl -6 -REST_Commands http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/paths/

Data retrieved is in __JSON__ format

* __/routes__ or __/routes/__: __GET__

		curl -g6 http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/routes

	_output_:

		{
			fountain:'IPv6_Address_Fountain',
			neighbors: [
					'IPv6Addr_1',
					'IPv6Addr_2',
					...
			]
		}

* __/gpio/status__ or __/gpio/status/__: __GET__

		curl -g6 http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/gpio/status

	_output_:

		{
			pinStatus: {
				{
					pin: 20,
					value: 1
				},
				{
					pin: 21,
					value: 1
				}
			}
		}


* __/gpio/pinNumber__ or __/gpio/pinNumber/__: __GET__ and __POST__

	__GET__:

		curl -g6 http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/gpio/20

						OR

		curl -g6 http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/gpio/21

	_output_:

		{
			pin: 20,
			value: 1
		}

	or

		{
			pin: 21,
			value: 0
		}

	__POST__: to change the GPIO value __/gpio/20/?value__

		curl -6 --data 'value=1' http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/gpio/20

						OR

		curl -6 --data 'value=0' http://[fe80::1abb:23ff:fecc:dd44%wlan0]:8080/gpio/21

	_output_:

		{
			pin: 20,
			newValue: 1
		}

	or

		{
			pin:21,
			newValue: 0
		}