class LogProcessor:
	def __init__(self, name):
		self.fileName = name

	def parse_file_to_log_var(self):
		self.log = []
		file = open(self.fileName)
		enc_txt_entry = False
		enc_short_txt_entry = False
		tmp_txt_enrty = []
		tmp_short_txt_enrty = []
		tmp_enrty = {}

		for line in file.readlines():
			if enc_txt_entry == True or enc_short_txt_entry == True:
				line = line.strip().replace('&nbsp', ' ').replace('\r', '').replace('\n', '').replace("'", '')
				if enc_short_txt_entry == True:
					if line.find(']') != -1:
						tmp_short_txt_enrty.append(line.replace(']', ''))
						tmp_enrty = {"detail":tmp_txt_enrty, "short":tmp_short_txt_enrty}
						self.log.append(tmp_enrty)
						enc_short_txt_entry = False
						tmp_enrty = {}
						tmp_txt_enrty = []
						tmp_short_txt_enrty = []
					else:
						tmp_short_txt_enrty.append(line.replace(',', ''))
				else:
					if line.find(']') != -1:
						tmp_txt_enrty.append(line.replace(']', ''))
						enc_txt_entry = False
					else:
						tmp_txt_enrty.append(line.replace(',', ''))
			else:
				#when hit the bottom of the log
				if line.find('tbl_AllDetails') != -1:
					break
				elif line.find('ShortTxtEntry') != -1 and line.find('= [') != -1:
					enc_short_txt_entry = True
				elif line.find('TxtEntry') != -1 and line.find('= [') != -1:
					enc_txt_entry = True

		file.close()

		return self.log
		# self.print_var_log_short()
		# self.print_var_log_detail()

	def print_var_log_short(self):
		tmpFile = open("var_log_short.txt", "w")
		for i in range(len(self.log)):
			print(self.log[i]["short"])
			tmpFile.write(str(self.log[i]["short"])+'\r\n')
		tmpFile.close()

	def print_var_log_detail(self):
		tmpFile = open("var_log_detail.txt", "w")
		for i in range(len(self.log)):
			print(self.log[i]["detail"])
			tmpFile.write(str(self.log[i]["detail"])+'\r\n')
		tmpFile.close()

	def show_test(self):
		DetailsTxt = ["123","456","789"]
		ShortTxt = ["abc","def","ghi"]

		entry = {"detail":DetailsTxt, "short":ShortTxt}
		log = [entry]
		print(log)

		DetailsTxt = ["111","222","333"]
		ShortTxt = ["aaa","bbb","ccc"]
		entry = {"detail":DetailsTxt, "short":ShortTxt}
		log.append(entry)
		print(log)

		item = log[0]
		print(item["detail"])
		print(item["short"])
		detailTxt = item["detail"]
		print(detailTxt[0])
		shortTxt =item["short"]
		print(shortTxt[0])

		item = log[1]
		print(item["detail"])
		print(item["short"])