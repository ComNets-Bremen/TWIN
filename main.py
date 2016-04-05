#!/usr/bin/env python

from sys import argv, exit
from Server import server
from Receiver import receiver




def main():
	if len(argv) < 2:
		print "use python main.py -h or python main.py --help"
		exit(1)

	if argv[1] == '-h' or argv[1] == '--help':
		print """Script performs accordingly.\n
		USAGE: python main.py [-sr] /home/myFolder/ file.ihex \n

		OPTIONS:
			-s or --server : to send code into network
			* Add the Path and File to be uploaded successively
			
			-r or --receiver : to receive code from server
		"""
		exit(1)


	elif argv[1] == '-s' or argv[1] == '--server':
		if (len(argv) < 3):
			print "Insert Path of the File and the File to be Uploaded. Use -h or --help" \
			" for USAGE"	
			exit(1)
		PATH = argv[2]
		FILENAME = argv[3]
		server(PATH, FILENAME)

	elif argv[1] == '-r' or argv[1] == '--receiver':
		receiver()

	





if __name__ == "__main__":
	main()
