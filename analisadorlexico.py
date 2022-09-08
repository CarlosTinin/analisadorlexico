from processor import Processor

def main():
	file = open_file('teste_codigo.tinin');
	
	if(file):
		proc = Processor() 
		proc.process_file(file)

		print(proc.show_token_list())

	file.close()

def open_file(file_name):
	try:
		file = open(r"{}".format(file_name), "r")
	except FileNotFoundError:
		print("Arquivo não encontrado!")
	else:
		return file

main()