import sys
sys.path.append("../")
from lexico.analisadorlexico import analiseLexica
from processor import Processor

def analiseSintatica():
	result = {}
	lexicalList = analiseLexica()
	for input_file in lexicalList:
		proc = Processor() 
		#print("\n\______________________________________ "+input_file+" ______________________________________/\n")
		proc.process_tokens(lexicalList[input_file])
		result[input_file] =proc.errors_list()
		save_file(input_file, proc.errors_list())
		proc.reset()
		

def save_file(file_name, errors_list):
    file = open("../files/syntactic-outputs/"+file_name, 'w+', encoding = "UTF-8")
    if not errors_list:
        file.write("Executado com sucesso!")
    else:
        for erro in errors_list:
            file.write(str(erro)+"\n")
    file.close()


analiseSintatica()