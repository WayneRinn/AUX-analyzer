#!/usr/bin/env python
import os
import sys

from LogProcessor import LogProcessor

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("usage: './AuxParser.py fileName'")
	elif len(sys.argv) == 2:
		if os.path.isfile(str(sys.argv[1])):
			aux_log = LogProcessor(str(sys.argv[1]))
			aux_log.parse_file_to_log_var()
		else:
			print("file doesn't exit")
