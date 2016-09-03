## Data Retrieval

Every `config.ini` has two parameter for each __TWIN Node__:

* `file` : Specifies which `.ihex` file dedicated for the respective TWIN Node

* `time` : Specified in __24-Hour__ format as to when each TWIN Node would send collected
information in the `~/outgoing/` folder to the nearest known *Fountain*

### Example

	[node1]
	file = File_1.ihex
	time = 12:30

	[node2]
	file = File_2.ihex
	time = 15:00

	....

## Files

* `configuration.py` : Parses the `.tar` file for a `config.ini` and does the following:

	* extract the dedicated `.ihex` to a dedicated `~/bsl` folder

	* create a scheduler for sending data in the `~/outgoing` folder to the nearest Fountain

* `scheduleSend.py` : sets a scheduler at the specified `time` in the `config.ini`

