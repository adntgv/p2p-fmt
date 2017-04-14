# p2p-fmt
Designed to wirk with python3.5
The code has been tested on Ubuntu Linux
Required libraries:

import socket
import os
import json
import sys
import re
import selectors
import time
import threading


The fmt.pt - server appplication has to be ran first. After that initialize client.py $(folder) $(port). where folder is a directory containing shared files and port is a number of port to work with.

Implemented commands:

	SEARCH - search for a $(filename) without file extension. 
				Possible to search for $(ext) files. 
			Example:
				SEARCH ACDC - Thunderstruck 
				SEARCH .mp3 
	LIST - list all files shared with this server

	DOWNLOAD - download a file from peer, arguments separated by period,
				into a $(folder).
				Required arfuments: filename(with extension), ip, port
			Example:
				DOWNLOAD,ACDC - Thunderstruck,192.168.1.1,5555
			
