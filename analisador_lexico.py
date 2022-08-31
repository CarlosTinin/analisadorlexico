import re

def main():
	file = open_file('teste_codigo.tinin');
	
	if(file):
		process_file(file)

	file.close()

def open_file(file_name):
	try:
		file = open(r"{}".format(file_name), "r")
	except FileNotFoundError:
		print("Arquivo não encontrado!")
	else:
		return file

def process_file(file):
	for line in file.readlines():
		for char in line:
			if(re.match(r'[A-Z]|[a-z]', char)):
				print(char)
		break

main()