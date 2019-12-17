#!/usr/bin/env python
import os
import sys

from LogProcessor import LogProcessor
from AuxEventProcessor import AuxEventProcessor


def show_functionality():
	print('show_functionality\n')
	pass

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("usage: './AuxParser.py fileName [-optinos]'")
		sys.exit()

	if os.path.isfile(str(sys.argv[1])):
		pass
	else:
		print("file doesn't exit")
		sys.exit()

	aux_log = LogProcessor(str(sys.argv[1]))
	log = aux_log.parse_file_to_log_var()
	aux_event_pro = AuxEventProcessor(log)

	if str(sys.argv[2]) == "-la":
		aux_event_pro.get_last_allocate_payload_result()
	elif str(sys.argv[2]) == "-en":
		if len(sys.argv) > 3:
			line = int(str(sys.argv[3]))
		else:
			line = 0
		aux_event_pro.get_enum_path_result_from_line(line)
	elif str(sys.argv[2]) == "-ri2c":
		aux_event_pro.get_remote_i2c_read_result()
	elif str(sys.argv[2]) == "-err":
		aux_event_pro.get_any_error_from_log()
	elif str(sys.argv[2]) == "-lk":
		if len(sys.argv) > 3:
			line = int(str(sys.argv[3]))
		else:
			line = 0
		aux_event_pro.get_link_address_result(line)
	elif str(sys.argv[2]) == "-lt":
		if len(sys.argv) > 3:
			line = int(str(sys.argv[3]))
		else:
			line = 0
		aux_event_pro.get_link_training_result_from_line(line)
	else:
		analyzing_str_line = str(sys.argv[2])
		print("start analyze Aux report")
		show_functionality()
		choose = raw_input('select the function:\n')
		quit = 'q'

		while(choose != quit):
			aux_event_pro.get_last_allocate_payload_result()
			aux_event_pro.get_enum_path_result_from_line(0)
			# aux_event_pro.get_remote_i2c_read_result()
			# aux_event_pro.get_last_0x111_mstm_ctrl()
			# aux_event_pro.get_any_error_from_log()
			show_functionality()
			choose = raw_input('select the function:\n')
