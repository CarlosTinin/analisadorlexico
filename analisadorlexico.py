from processor import Processor
import os

class AnalisadorLexico:
	def __init__(self):
		self.proc = Processor() 
		self.tokens = []
	def run(self):
		for  directory, subdirs, files in os.walk("files/inputs"):
			for input_file in files:
				file = self.open_file(directory+"/"+input_file)
				if(file):
					self.proc.process_file(file)
					self.save_file(input_file, self.proc.show_token_list())
					self.tokens.append({"file": input_file, "tokens":self.proc.show_token_list()})
				file.close()
		return self.tokens

	def open_file(self, file_name):
		try:
			file = open(r"{}".format(file_name), "r")
		except FileNotFoundError:
			print("Arquivo não encontrado!")
		else:
			return file

	def save_file(self, file_name, token_list):
		file = open("files/outputs/"+file_name, 'w+')
		errors="\n"
		for token in token_list:
			
			token_line= token['line'].zfill(2)+" "+token['category']+" "+token['content']+"\n"
			#stores all errors to append in the end of file
			if ("ERROR" in token['type']  or "INVALID" in token['type']):
				errors += token_line
			else :
				if("COMMENT" not in token['type']):
					file.write(token_line)

		file.write(errors)
		file.close()


	#main()