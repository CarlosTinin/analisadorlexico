from lexico.processor import Processor
import os

def analiseLexica():
	result = {}
	for  directory, subdirs, files in os.walk("files/inputs"):
		for input_file in files:
			file = open_file(directory+"/"+input_file)
			if(file):
				proc = Processor() 
				proc.process_file(file)
				#save_file(input_file, proc.show_token_list())
				result[input_file] = proc.show_token_list()

			file.close()

	return result

def open_file(file_name):
	try:
		file = open(r"{}".format(file_name), "r")
	except FileNotFoundError:
		print("Arquivo não encontrado!")
	else:
		return file

def save_file(file_name, token_list):
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