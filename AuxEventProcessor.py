class AuxEventProcessor:
	def __init__(self, log):
		self.log = log

	def get_idx_of_particular_string_in_log_short_from_line(self, str_to_find, str_idx):
		for idx in range(str_idx, len(self.log)):
			short_msg = self.log[idx]["short"][0]
			if short_msg.find(str_to_find) != -1:
				return idx
		return False

	def get_idx_of_particular_dpcd_addr_value_in_log_detail_from_line(self, addr_to_find, value, str_idx):
		for idx in range(str_idx, len(self.log)):
			short_msg = self.log[idx]["short"][0]
			if short_msg.find(addr_to_find) != -1:
				detail_msg = self.log[idx]["detail"][4]
				detail_msg_seg = detail_msg.split('<br>')
				for idx2 in range(0, len(detail_msg_seg)):
					if detail_msg_seg[idx2].find(value) != -1:
						return idx
		return False

	def get_idx_of_last_particular_string_in_log_short(self, str_to_find):
		for idx in range(len(self.log) - 1, -1, -1):
			short_msg = self.log[idx]["short"][0]
			if short_msg.find(str_to_find) != -1:
				return idx
		return False


	def get_last_0x111_mstm_ctrl(self):
		ret_idx = self.get_idx_of_last_particular_string_in_log_short("to 0x00111")
		if  ret_idx != False:
			last_item_idx = len(self.log[ret_idx]["detail"]) - 1
			detail_msg = self.log[ret_idx]["detail"][last_item_idx]
			detail_msg_seg = detail_msg.split('<br>')
			for idx in range(0, len(detail_msg_seg)):
				if detail_msg_seg[idx].find("MST_EN") != -1:
					mst_en_line = detail_msg_seg[idx].split()
					mst_en_value = mst_en_line[2]
				if detail_msg_seg[idx].find("UP_REQ_EN") != -1:
					up_req_en_line = detail_msg_seg[idx].split()
					up_req_en_value = up_req_en_line[2]
			if self.log[ret_idx + 1]["short"][0].find('AUX_ACK') != -1:
				return {"line":ret_idx,"mst_en_value":mst_en_value, "up_req_en_value":up_req_en_value}
			else:
				return False
		else:
			return ret_idx


	# backwards find allocate payload msg and break when meet the ENUM_PATH_RESOURCES
	def get_last_allocate_payload_result(self):
		find_allocate_payload_msg = False
		for idx_of_allocate_payload_msg in range(len(self.log) - 1, -1, -1):
			short_msg = self.log[idx_of_allocate_payload_msg]["short"][0]
			if short_msg.find('REPLY: ALLOCATE_PAYLOAD') != -1:
				find_allocate_payload_msg = True
				print('The last ALLOCATE_PAYLOAD occur at line:' + str(idx_of_allocate_payload_msg + 1))
				# detail data is fixed at ["detail"][4]
				detail_msg = self.log[idx_of_allocate_payload_msg]["detail"][4]
				detail_msg_seg = detail_msg.split('<br>')
				for idx in range(0, len(detail_msg_seg)):
					if (detail_msg_seg[idx].find("Link_Count_Total") != -1 or
						detail_msg_seg[idx].find("Port_Number") != -1 or
						detail_msg_seg[idx].find("Virtual_Channel_Payload_ID") != -1 or
						detail_msg_seg[idx].find("Payload_Bandwitdh_Number") != -1):
						print(detail_msg_seg[idx])
				print('\n')
			# currently use ENUM_PATH_RESOURCES to seperate different cycle of allocating payload
			if short_msg.find('REPLY: ENUM_PATH_RESOURCES') != -1:
				break

		return find_allocate_payload_msg

	def get_remote_i2c_read_result(self):
		find_remote_i2c_msg = False
		result = []
		tmp_str = ""

		# get I2C read slave addr and offset
		for idx_of_remote_i2c_req in range(len(self.log) - 1, -1, -1):
			short_msg = self.log[idx_of_remote_i2c_req]["short"][0]
			if short_msg.find('REQ: REMOTE_I2C_READ') != -1:
				last_item_idx = len(self.log[idx_of_remote_i2c_req]["detail"]) - 1
				detail_msg = self.log[idx_of_remote_i2c_req]["detail"][last_item_idx]
				detail_msg_seg = detail_msg.split('<br>')
				for idx in range(0, len(detail_msg_seg)):
					if (detail_msg_seg[idx].find("Link_Count_Total") != -1 or
						detail_msg_seg[idx].find("Port_Number") != -1 or
						detail_msg_seg[idx].find("Write_I2C_Device_ID") != -1 or
						detail_msg_seg[idx].find("Number_Of_Bytes_To_Write") != -1 or
						detail_msg_seg[idx].find("Data Dump:") != -1):
						tmp_str = tmp_str + detail_msg_seg[idx] + "\n"
						if detail_msg_seg[idx].find("Data Dump:") != -1:
							for idx2 in range(idx + 1, len(detail_msg_seg) - 1):
								if detail_msg_seg[idx2].find('-- I2C Read') != -1:
									break
								tmp_str = tmp_str + detail_msg_seg[idx2] + "\n"
							break

				find_remote_i2c_msg = False
				for idx_of_remote_i2c_repl in range(idx_of_remote_i2c_req + 1, len(self.log)):
					short_msg = self.log[idx_of_remote_i2c_repl]["short"][0]
					if short_msg.find('REPLY: REMOTE_I2C_READ') != -1:
						find_remote_i2c_msg = True
						last_item_idx = len(self.log[idx_of_remote_i2c_repl]["detail"]) - 1
						detail_msg = self.log[idx_of_remote_i2c_repl]["detail"][last_item_idx]
						detail_msg_seg = detail_msg.split('<br>')
						for idx in range(0, len(detail_msg_seg)):
							if (detail_msg_seg[idx].find("Number_Of_Bytes_Read") != -1 or
								detail_msg_seg[idx].find("Data_Read Dump") != -1):
								# print(detail_msg_seg[idx])
								tmp_str = tmp_str + detail_msg_seg[idx] + "\n"
								if detail_msg_seg[idx].find("Data_Read Dump") != -1:
									for idx2 in range(idx + 1, len(detail_msg_seg) - 1):
										# print(detail_msg_seg[idx2])
										tmp_str = tmp_str + detail_msg_seg[idx2] + "\n"
									break
						result.append(tmp_str + "---")
						tmp_str = ""
						# print('\n')
						break

				if find_remote_i2c_msg == False:
					return False

		for idx in range(len(result) - 1, -1, -1):
			print(result[idx])

		return find_remote_i2c_msg

	def get_enum_path_result_from_line(self, start_line_num):
		find_enum_path_msg = False

		for idx_of_enum_path_msg in range(start_line_num, len(self.log)):
			short_msg = self.log[idx_of_enum_path_msg]["short"][0]
			if short_msg.find('REPLY: ENUM_PATH_RESOURCES') != -1:
				find_enum_path_msg = True
				print('Find ENUM_PATH reply at line:' + str(idx_of_enum_path_msg + 1))
				# detail data is fixed at ["detail"][4]
				detail_msg = self.log[idx_of_enum_path_msg]["detail"][4]
				detail_msg_seg = detail_msg.split('<br>')
				for idx in range(0, len(detail_msg_seg)):
					if (detail_msg_seg[idx].find("Link_Count_Total") != -1 or
						detail_msg_seg[idx].find("Port_Number") != -1 or
						detail_msg_seg[idx].find("Full_Payload_Bandwidth_Number") != -1 or
						detail_msg_seg[idx].find("Available_Payload_Bandwidth_Number") != -1):
						print(detail_msg_seg[idx])
				print('\n')

		return find_enum_path_msg

	def get_link_address_result(self, start_line_num):
		find_link_address_msg = False
		print('---\n')
		for idx_of_link_addr_msg in range(start_line_num, len(self.log)):
			short_msg = self.log[idx_of_link_addr_msg]["short"][0]
			if short_msg.find('REPLY: LINK_ADDRESS') != -1:
				find_link_address_msg = True
				print('Find LINK_ADDRESS reply at line:' + str(idx_of_link_addr_msg + 1))
				# detail data is fixed at ["detail"][4]
				detail_msg = self.log[idx_of_link_addr_msg]["detail"][4]
				detail_msg_seg = detail_msg.split('<br>')
				for idx in range(0, len(detail_msg_seg)):
					if detail_msg_seg[idx].find("Link_Count_Total") != -1:
						print(detail_msg_seg[idx])
					if detail_msg_seg[idx].find("Number_Of_Ports") != -1:
						for idx2 in range(idx, len(detail_msg_seg) - 1):
							print(detail_msg_seg[idx2])
						break
				print('\n---\n')

		return find_link_address_msg

	def get_link_training_result_from_line(self, line_num):
		# 0x00102 to set training pattern
		find_lt_msg = False
		str_idx = line_num
		lt_str_idx = self.get_idx_of_particular_string_in_log_short_from_line("to 0x00102", str_idx)
		while lt_str_idx != False:
			lt_end_idx = self.get_idx_of_particular_dpcd_addr_value_in_log_detail_from_line("to 0x00102", "0x00102 := 0x00", lt_str_idx)
			if lt_end_idx == False:
				print("Can't find the end of LT\n")
				return find_lt_msg
			# interval of LT
			find_lt_msg = True
			print('---\n')
			print("Find LT start at line:" + str(lt_str_idx + 1) + " and end at line:" + str(lt_end_idx + 1) +"\nLT final result:\n")
			for idx in range(lt_end_idx -1, lt_str_idx, -1):
				short_msg = self.log[idx]["short"][0]
				if short_msg.find('to 0x00102') != -1:
					detail_msg = self.log[idx]["detail"][4]
					detail_msg = detail_msg.replace("</p>","<br>")
					detail_msg_seg = detail_msg.split('<br>')
					for idx2 in range(0, len(detail_msg_seg)):
						if (detail_msg_seg[idx2].find("Line #") != -1 or
							detail_msg_seg[idx2].find("Req WR") != -1):
							continue
						print(detail_msg_seg[idx2])
					break;
			for idx3 in range(lt_end_idx -1, lt_str_idx, -1):
				short_msg = self.log[idx3]["short"][0]
				if short_msg.find('from 0x00202') != -1:
					detail_msg = self.log[idx3 + 1]["detail"][4]
					detail_msg = detail_msg.replace("</p>","<br>")
					detail_msg_seg = detail_msg.split('<br>')
					for idx4 in range(0, len(detail_msg_seg)):
						if (detail_msg_seg[idx4].find("Line #") != -1 or
							detail_msg_seg[idx4].find("AUX_ACK") != -1):
							continue
						print(detail_msg_seg[idx4])
					break;

			str_idx = lt_end_idx + 1
			lt_str_idx = self.get_idx_of_particular_string_in_log_short_from_line("to 0x00102", str_idx)
		return find_lt_msg

	def get_payload_table_from_line(self, line_num):
		pass

	def get_all_side_band_msg_from_line(self, line_num):
		pass

	def get_any_error_from_log(self):
		for idx in range(0, len(self.log)):
			last_item_idx = len(self.log[idx]["detail"]) - 1
			detail_msg = self.log[idx]["detail"][last_item_idx]
			detail_msg_seg = detail_msg.split('<br>')
			for idx2 in range(0, len(detail_msg_seg)):
				if detail_msg_seg[idx2].find("Error") != -1:
					print("Find error msg in line " + str(idx) + ":\n"
						+ detail_msg_seg[idx2] + "\n")


