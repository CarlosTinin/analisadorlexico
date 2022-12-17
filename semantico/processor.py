RED   = "\033[1;31m"  
YEL = "\033[1;33m"  
RESET = "\033[0;0m"
type = None
ide = None
content = None
result=None
content_type = None
tokens_list = []
token_index = 0
identify_value = -1
syntatic_errors_list = []
semantic_errors_list = []
start_procedure_flag = False
declaration_flag = False
first_matrix = ["IDE"]
first_term_rest = ["*", "/"]
first_function_call = ["IDE"]
first_expression_rest = ["+", "-"]
follow_logic_value = [ '&&', '||']
first_expression = ["IDE", "NRO", "("]
first_type = ['int','real','boolean','string', "IDE"]
follow_relacional_value = [ '!=' , '==' , '<' , '<=' , '>' , '>=' , '=']
first_logic_expression = ["!", "IDE", "NRO", "CAC", "(", "true", "false"]
first_relational_expression = ["IDE", "NRO", "CAC", "(", "true", "false"]
first_start = ["struct","read","print","while","if","function","procedure","var","const","!","(","{","IDE"]
first_block = first_logic_expression + ["print","read","while", "if","var","const"]

var_symbols_list = []
func_symbols_list = []
params_symbols_list = []
all_symbols = []

class Processor:
	def __init__(self):
		self.tokens_list = []
		self.token_index = 0
		self.var_symbols_list = []
		#self.errors_list = []

	def syntactic_errors_list(self):
		global syntatic_errors_list
		return syntatic_errors_list
	
	def semantic_errors_list(self):
		global semantic_errors_list
		return semantic_errors_list
	
	def reset(self):
		global tokens_list, result,all_symbols, token_index, start_procedure_flag, syntatic_errors_list,semantic_errors_list
		tokens_list = []
		token_index = 0
		semantic_errors_list = []
		syntatic_errors_list = []
		start_procedure_flag = False
		all_symbols = []
		result =[]

	def process_tokens(self, tokens):
		global tokens_list, params_symbols_list
		tokens_list=tokens
		start()


def insert_var_declaration(insertion):
	global var_symbols_list, type, ide, content
	var_symbols_list.append(insertion)	
	all_symbols.append(insertion)	
	#type = None
	ide = None
	content = None

def insert_func_declaration(insertion):
	global func_symbols_list, type, ide
	func_symbols_list.append(insertion)
	all_symbols.append(insertion)
	#type = None
	ide = None

def insert_params_declaration(insertion):
	global params_symbols_list, type, ide
	params_symbols_list.append(insertion)
	all_symbols.append(insertion)
	#type = None
	ide = None

def search_declaration(token):
	for declaration in all_symbols:
		if token['content'] in declaration:
			return declaration
	return [False, token]

#***********************************************************************************************
# START
#***********************************************************************************************
def start():
	global tokens_list, token_index
	while token_index < len(tokens_list)-1: #se não for o ultimo da lista
		#seleciona qual procedimento seguir de acordo com os simbolos que podem iniciar a gramática
		if tokens_list[token_index]['content'] == "struct":
			Struct()
		elif tokens_list[token_index]['content'] == "read": 
			Read()
		elif tokens_list[token_index]['content'] == "print": 
			Print()
		elif tokens_list[token_index]['content'] == "while": 
			While()
		elif tokens_list[token_index]['content'] == "if": 
			If()
		elif tokens_list[token_index]['content'] == "function": 
			function()
		elif tokens_list[token_index]['content'] == "procedure": 
			procedure()
		elif tokens_list[token_index]['content'] == "var": 
			Var()
		elif tokens_list[token_index]['content'] == "const": 
			Const()
		elif tokens_list[token_index]['content'] == "!": 
			logicExpression()
		elif tokens_list[token_index]['content'] == "(": 
			identify()
		elif tokens_list[token_index]['content'] == "{": 
			block()
		elif tokens_list[token_index]['category'] == "IDE":
			identify()
		elif tokens_list[token_index]['category'] == "NRO":
			number()
		else :
			errorRecovery(tokens_list[token_index], first_start)

#***********************************************************************************************
# CONST  E  VAR
#***********************************************************************************************
def Const():
	if('const'== tokens_list[token_index]['content']): #verifica se o token atual é 'conts'
		print(tokens_list[token_index]['content'], end=" ")
		next()
		declarationBlock() #chama o bloco de declaracao de variaveis {int a, b=0; boolean v; }
	else:
		errorRecovery(tokens_list[token_index], [])
		

def Var():
	if('var'== tokens_list[token_index]['content']):#verifica se o token atual é 'var'
		print(tokens_list[token_index]['content'], end=" ")
		next()
		declarationBlock()#chama o bloco de declaracao de variaveis {int a, b=0; boolean v; }
	else:
		errorRecovery(tokens_list[token_index], [])

def declarationBlock():
	global type
	if('{' == tokens_list[token_index]['content']): #verifica se o token atual é '{'
		print(tokens_list[token_index]['content'])
		next()
	else: # se o token não for '{'
		errorRecovery(tokens_list[token_index], first_type) #imprime o erro e vai para o seguinte de '{' que é ['int','real','boolean','string', "IDE"]
	allVars() #continual chamando a funçao que analisa a declaracao das variaveis
	matchCloseCBrackets()
	type = None

def allVars():
	global type
	if tokens_list[token_index]['content'] in first_type or tokens_list[token_index]['category'] in first_type: # verifica se o token é um tipo ['int','real','boolean','string', "IDE"]
		print(tokens_list[token_index]['content'], end=" ")
		type = tokens_list[token_index]['content'] #guarda o tipo
		next()
		varList() # funcao que verifica as variaveis declaradas
	else : #se o token não for um tipo
		errorRecovery(tokens_list[token_index], first_type+[";"])  #imprime o erro e vai para o seguinte do tipo que pode ser outros tipos ou ';' 
		allVars()#continual chamando a funçao que analisa a declaracao das variaveis

def varList():
	global ide
	if tokens_list[token_index]['category'] == "IDE": # se o token é um identificador
		print(tokens_list[token_index]['content'], end=" ")
		ide = tokens_list[token_index]['content'] #guarda o identificador
		#print("\n\n"+RED+ide+RESET+"\n\n")
		next()
		varListSeparation() # funcao que analisa atribuicao ou lista de variáveis: a=10, b, i=0 
		commaSeparation()
	else : #se o token não for um identificador
		errorRecovery(tokens_list[token_index], [";", ","])
		commaSeparation() # funcao que analisa atribuicao ou lista de variaveis: a=10, b, i=0

def  commaSeparation():
	global type, content, ide
	insert_var_declaration([type, ide, content, tokens_list[token_index]['line']]) #insere na lista de variaveis
	if tokens_list[token_index]['content'] == ",": #se o proximo token for ','
		print(tokens_list[token_index]['content'], end=" ")
		next()
		varList() # continua na analise das variáveis
	else :
		if tokens_list[token_index]['content'] == ";":
			print(tokens_list[token_index]['content'])
			next()
			if tokens_list[token_index]['content'] in first_type or tokens_list[token_index]['category'] in first_type: #se o token for um tipo
				allVars()
		else :
			if tokens_list[token_index-1]['content'] == ";" and tokens_list[token_index]['content'] == "}":
				matchCloseCBrackets
			else:
				errorRecovery(tokens_list[token_index], ["}", ",", ";"])
				if tokens_list[token_index]['content'] in first_type or tokens_list[token_index]['category'] in first_type: #se o token for um tipo
					allVars() # chama funcao que trata as declaracões
				elif tokens_list[token_index]['content'] == ",":
					varList()

def varListSeparation():
	global content, type, result
	if tokens_list[token_index]['content'] == "=": # se token for o operador de atribuiçao
		print(tokens_list[token_index]['content'], end=" ")
		next()
		content = tokens_list[token_index]['content'] # guarda o conteudo
		if tokens_list[token_index]['category'] == "NRO": # verifica se é um número
			result = [type, ide, content]
			number()
		elif tokens_list[token_index]['content'] == "false" or tokens_list[token_index]['content'] == "true": # verifica se é um boleano
			print(tokens_list[token_index]['content'], end=" ")
			result = [type, ide, content]
			if type != "boolean":
				hasError(tokens_list[token_index], 'boolean')
			next()
		elif tokens_list[token_index]['category'] == "CAC":
			print(tokens_list[token_index]['content'], end=" ")
			result = [type, ide, content]
			hasError(tokens_list[token_index], 'string')
			next()
		elif tokens_list[token_index]['content'] == "[":
			matrix()
		else : # se não for numero é identificador
			identify()
			if result and result[0]!=type  and tokens_list[token_index-1]['category'] != "DEL":
				hasError(tokens_list[token_index-1], type)
		
def assignment():
	global result
	if tokens_list[token_index]['content'] == "=": # se o token for operador de atribuiçao
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if tokens_list[token_index]['category'] == "NRO":
			number()
			matchSemicolon()
		elif tokens_list[token_index]['category'] == "CAC":
			print(tokens_list[token_index]['content'], end=" ")
			next()
			matchSemicolon()
		elif tokens_list[token_index]['category'] == "IDE":
			var_type = result[0]
			identify()
			# o tipo da variavel que recebe o valor for diferente do tipo do valor
			if var_type and var_type != result[0]:
				hasError(tokens_list[token_index-1], var_type)
			if ('.' in identify_value or tokens_list[token_index-1]['category'] != "NRO") and tokens_list[token_index-1]['category'] != "IDE" and tokens_list[token_index-1]['category'] != "DEL":
				result = ["int", None, None]
			#	hasError(tokens_list[token_index-1], "int")
	#elif result[0] and result[0] !="int" and tokens_list[token_index-1]['category'] != "DEL":
	#	hasError(tokens_list[token_index-1], "int")
			#se for chamda de função não dá match no nesse momento
			if len(result)==3:
				pass
			else:
				matchSemicolon()
		else :
			errorRecovery(tokens_list[token_index], [])
			#errorRecovery(error, ["PRE", "IDE"])
	else :
		errorRecovery(tokens_list[token_index], [])
		#errorRecovery(error, ["PRE", "IDE"])

#***********************************************************************************************
# MATRIZ
#***********************************************************************************************
def matrix():
	access()
	if('['== tokens_list[token_index]['content']): # verifica se há um segundo '[', para formar a[1][2]
		access()

def access():
	if('['== tokens_list[token_index]['content']): 
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matrixIndex()
	else:
		errorRecovery(tokens_list[token_index], [";", ","]+ first_type)

def matrixIndex():
	global result
	identify()
	#if ('.' in identify_value or tokens_list[token_index-1]['category'] != "NRO") and tokens_list[token_index-1]['category'] != "IDE" and tokens_list[token_index-1]['category'] != "DEL":
		#result = ["int", None, None]
	#	hasError(tokens_list[token_index-1], "int")
	#elif result[0] and result[0] !="int" and tokens_list[token_index-1]['category'] != "DEL":
	#	hasError(tokens_list[token_index-1], "int")
		

	if(']'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
	else :
		errorRecovery(tokens_list[token_index], [";", ","]+ first_type)
	
#***********************************************************************************************
# STRUCT
#***********************************************************************************************
def Struct():
	global tokens_list, token_index

	if('struct'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('IDE' == tokens_list[token_index]['category']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			structBlock()
		else:
			errorRecovery(tokens_list[token_index], ["{"]+ first_type)
			structBlock()
	else:
		errorRecovery(tokens_list[token_index], [])

def structBlock():
	if('{' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next()
	else:
		errorRecovery(tokens_list[token_index], first_type)
	allVars()
	matchCloseCBrackets()

def compType():
	if('.' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('IDE' == tokens_list[token_index]['category']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
		else:
			errorRecovery(tokens_list[token_index], [";", ",", ")", "}"])
	else :
		errorRecovery(tokens_list[token_index], [])

#***********************************************************************************************
# EXTENDS
#***********************************************************************************************
def Extends():
	global tokens_list, token_index
	if('extends'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('IDE' == tokens_list[token_index]['category']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			extendsBlock()
		else:
			errorRecovery(tokens_list[token_index], [])
			#errorRecovery(error, ["PRE", "IDE"])
	else:
		errorRecovery(tokens_list[token_index], [])
		
def extendsBlock():
	if('{' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next()	
	else:
		errorRecovery(tokens_list[token_index], first_type)
	allVars()
	matchCloseCBrackets()

#***********************************************************************************************
# READ
#***********************************************************************************************
def Read(): 
	global tokens_list, token_index
	
	if('read'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('(' == tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			readContent()
		else:
			errorRecovery(tokens_list[token_index], ["IDE"])
			readContent()
	else:
		errorRecovery(tokens_list[token_index], [])

def readContent():
	identify()
	#next()
	if(')' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matchSemicolon()
	else:
		errorRecovery(tokens_list[token_index], [";", "}"]+first_type)
		matchSemicolon()

def matchSemicolon():
	if(';' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next()
	else:
		errorRecovery(tokens_list[token_index], ["PRE", "IDE"])
		#start()

#***********************************************************************************************
# PRINT
#***********************************************************************************************
def Print(): 
	global tokens_list, token_index

	if('print'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('(' == tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			printContent()
		else:
			errorRecovery(tokens_list[token_index], ["IDE", "CAC"])
			readContent()
	else:
		errorRecovery(tokens_list[token_index], [])
		#errorRecovery(error, ["PRE", "IDE"])

def printContent():
	if 'IDE' == tokens_list[token_index]['category']:
		identify()
	elif 'CAC' == tokens_list[token_index]['category']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
	else:
		errorRecovery(tokens_list[token_index], [";", "}", ")"])

	if(')' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matchSemicolon()
	else:
		errorRecovery(tokens_list[token_index], [";", "}"]+first_type)
		matchSemicolon()

#***********************************************************************************************
# WHILE
#***********************************************************************************************
def While(): 
	global tokens_list, token_index

	if('while'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('(' == tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			whileContent()
		else:
			errorRecovery(tokens_list[token_index], ["IDE", ")", "{"])
			whileContent()
	else :
		errorRecovery(tokens_list[token_index], [])

def whileContent():
	identify()
	if(')' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matchOpenBlock()
	else :
		errorRecovery(tokens_list[token_index], ["{", "PRE"]+first_type)
		matchOpenBlock()

#***********************************************************************************************
# IF
#***********************************************************************************************
def If():
	if('if'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('(' == tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			ifContent()
		else:
			errorRecovery(tokens_list[token_index], ["IDE", ")", "{"])
			ifContent()
	else :
		errorRecovery(tokens_list[token_index], [])

def ifContent():
	identify()
	if(')' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matchThen()
	else :
		errorRecovery(tokens_list[token_index], ["then", "{"])
		matchThen()

def matchThen():
	if('then' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matchOpenBlock()
		if('else' == tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'])
			next()
			matchOpenBlock()
	else :
		errorRecovery(tokens_list[token_index], ["{", "PRE"]+first_type)
		matchOpenBlock()

#***********************************************************************************************
# FUNCTION
#***********************************************************************************************
def function():
	global type
	if('function'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if(tokens_list[token_index]['content'] in first_type): # verifica se o token é um tipo
			print(tokens_list[token_index]['content'], end=" ")
			type = tokens_list[token_index]['content']
			next()
			functionName() 
		else :
			errorRecovery(tokens_list[token_index], ["IDE", "("])
			functionName()
	else :
		errorRecovery(tokens_list[token_index], [])

def functionName():
	global ide, type
	if('IDE' == tokens_list[token_index]['category']): #verifica se o token é um identificador
		print(tokens_list[token_index]['content'], end=" ")
		ide = tokens_list[token_index]['content']
		insert_func_declaration([type, ide, tokens_list[token_index]['line']])
		next()
		functionParamsBlock() 
	else :
		errorRecovery(tokens_list[token_index], ["("]+first_type)
		functionParamsBlock()

def functionParamsBlock():
	if('(' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		paramList()
		if(','== tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			paramList()
	else:
		errorRecovery(tokens_list[token_index], first_type+[")"])
		paramList()
	
	if(')' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		openFuncBlock()
		
	else:
		errorRecovery(tokens_list[token_index], ["{", "PRE"])
		openFuncBlock()

def paramList():
	global type, ide
	if(tokens_list[token_index]['content'] in first_type):
		print(tokens_list[token_index]['content'], end=" ")
		type = tokens_list[token_index]['content']
		next()
		if('IDE'== tokens_list[token_index]['category']):
			print(tokens_list[token_index]['content'], end=" ")
			ide = tokens_list[token_index]['content']
			insert_params_declaration([type, ide, tokens_list[token_index]['line']])
			next()
		else:
			errorRecovery(tokens_list[token_index], [",", ")", "{"])
			#verificar:
			if(','== tokens_list[token_index]['content']):
				print(tokens_list[token_index]['content'], end=" ")
				next()
				paramList()
	
def openFuncBlock():
	if('{' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next()
		block()
		matchFuncReturn() 
	else :
		errorRecovery(tokens_list[token_index], ["PRE", "IDE"])
		block()
		matchFuncReturn()

def matchFuncReturn():
	if('return' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		identify()
		matchEndReturn()
	else :
		errorRecovery(tokens_list[token_index], ["IDE", ";", "}"])

def matchEndReturn():
	if(';' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next() 
		matchCloseCBrackets()
	else :
		errorRecovery(tokens_list[token_index], [";", "}"])
		matchCloseCBrackets()

def parameters():
	if 'IDE' == tokens_list[token_index]['category'] :
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if '[' == tokens_list[token_index]['content']:
			matrix()
		elif '.' == tokens_list[token_index]['content']:
			compType()
		elif '(' == tokens_list[token_index]['content']:
			functionCall()
	elif 'NRO' == tokens_list[token_index]['category'] or 'CAC' == tokens_list[token_index]['category']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
	
	if ',' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		parameters()

def functionCall():
	if'(' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
	else :
		errorRecovery(tokens_list[token_index], ["IDE", "NRO", ",", ")"])
	parameters()
	
	if')' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		matchSemicolon()
	else :
		errorRecovery(tokens_list[token_index], [";", "PRE", "IDE"])

#***********************************************************************************************
# PROCEDURE
#***********************************************************************************************
def procedure():
	global start_procedure_flag
	if('procedure'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('IDE' == tokens_list[token_index]['category'] or ('start'== tokens_list[token_index]['content'] and not start_procedure_flag)):
			if 'start'== tokens_list[token_index]['content']:
				start_procedure_flag = True
			print(tokens_list[token_index]['content'], end=" ")
			next()
			procedParamsBlock()
		else :
			errorRecovery(tokens_list[token_index], ["("]+first_type)
			procedParamsBlock()
	else :
		errorRecovery(tokens_list[token_index], [])

def procedParamsBlock():
	if('(' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		paramList()
		if(','== tokens_list[token_index]['content']):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			paramList()
	else:
		errorRecovery(tokens_list[token_index], first_type+[")"])
		paramList()
	
	if(')' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		openProcedBlock()
		
	else:
		errorRecovery(tokens_list[token_index], ["{", "PRE"])
		openProcedBlock()

def openProcedBlock():
	if('{' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next()
		block()
		matchCloseCBrackets()
	else :
		errorRecovery(tokens_list[token_index], ["PRE", "IDE"])
		block()
		matchCloseCBrackets()

#***********************************************************************************************
# NUMERO
#***********************************************************************************************
def number():
	global tokens_list, token_index
	number = tokens_list[token_index]['content']
	print(tokens_list[token_index]['content'], end=" ")
	next()
	match tokens_list[token_index]['category']:
		case "ART":
			expression()
		case "REL": 
			relationalExpression()
		case "LOG": 
			logicExpression()
		case _:
			if '.' in tokens_list[token_index-1]['content']:
				hasError(tokens_list[token_index-1], 'float')
			elif 'NRO' == tokens_list[token_index-1]['category']:
				hasError(tokens_list[token_index-1], 'int')

#***********************************************************************************************
# EXPRESSÃO ARITIMETICA
#***********************************************************************************************
def expression():
	term()
	expressionRest()

def expressionRest():
	global tokens_list, token_index
	#token_index +=1
	if '+' == tokens_list[token_index]['content'] or '-' == tokens_list[token_index]['content'] and token_index<len(tokens_list)-1:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		factor()
		term()
		if '+' == tokens_list[token_index]['content'] or '-' == tokens_list[token_index]['content'] and token_index<len(tokens_list)-1:
			print(tokens_list[token_index]['content'], end=" ")
			next()
			factor()
		else :
			return

def term():
	global tokens_list, token_index
	#factor()
	termRest()

def termRest():
	global tokens_list, token_index
	
	if '*' == tokens_list[token_index]['content'] or '/' == tokens_list[token_index]['content'] and token_index<len(tokens_list):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		factor()
		if '*' == tokens_list[token_index]['content'] or '/' == tokens_list[token_index]['content'] and token_index<len(tokens_list):
			print(tokens_list[token_index]['content'], end=" ")
			next()
			factor()

def factor():
	global tokens_list, token_index
	
	if 'IDE' == tokens_list[token_index]['category'] or 'NRO' == tokens_list[token_index]['category'] and token_index<len(tokens_list):
		print(tokens_list[token_index]['content'], end=" ")
		
		#verifica o tipo do valor 
		if 'IDE' == tokens_list[token_index]['category']:
			value_type = search_declaration(tokens_list[token_index])
			hasError(tokens_list[token_index], value_type[0])
		elif '.' in tokens_list[token_index]['content']:
			hasError(tokens_list[token_index], 'float')
		else:
			hasError(tokens_list[token_index], 'int')

		next()
		#return
	elif '(' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		factor()
		expression()
		if ')' == tokens_list[token_index]['content']:
			print(tokens_list[token_index]['content'], end=" ")
			next()
			#return
	else :
		errorRecovery(tokens_list[token_index], ["*", "/", "+", "-"])
		identify()

#***********************************************************************************************
#EXPRESSÃO LÓGICA
#***********************************************************************************************
def logicExpression():
	global tokens_list, token_index

	if '!' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		logicValue()
	else :
		#logicValue()
		logicOperator()

def logicOperator():
	global tokens_list, token_index
	
	if '&&' == tokens_list[token_index]['content'] or '||' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		logicValue()
		if '&&' == tokens_list[token_index]['content'] or '||' == tokens_list[token_index]['content']:
			print(tokens_list[token_index]['content'], end=" ")
			next()
			logicValue()

def logicValue():
	global tokens_list, token_index, result
	
	if 'IDE' == tokens_list[token_index]['category'] or 'true' == tokens_list[token_index]['content'] or  'false' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		if 'IDE' == tokens_list[token_index]['category'] :
			result = search_declaration(tokens_list[token_index])
			hasError(tokens_list[token_index], 'boolean')
		next()
		return
	elif '(' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		logicValue()
		logicExpression()
		if ')' == tokens_list[token_index]['content']:
			print(tokens_list[token_index]['content'], end=" ")
			next()
			return
	else :
		errorRecovery(tokens_list[token_index], ["!", "&&", "||"])
		identify()

def negation():
	global tokens_list, token_index

	if '!' == tokens_list[token_index]['content']:
		next()
		logicValue()

#***********************************************************************************************
#EXPRESSÃO RELACIONAL
#***********************************************************************************************
def relationalExpression():
	relationalOperator()

def relationalOperator():
	global tokens_list, token_index
	if tokens_list[token_index]['content'] in follow_relacional_value:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		relationalValue()
		if tokens_list[token_index]['content'] in follow_relacional_value:
			print(tokens_list[token_index]['content'], end=" ")
			next()
			relationalValue()

def relationalValue():
	global tokens_list, token_index
	#print("$",tokens_list[token_index]['content'])
	if 'IDE' == tokens_list[token_index]['category'] or 'NRO' == tokens_list[token_index]['category'] or 'true' == tokens_list[token_index]['content'] or  'false' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")

		#verifica o tipo do valor 
		if 'IDE' == tokens_list[token_index]['category']:
			value_type = search_declaration(tokens_list[token_index])
			hasError(tokens_list[token_index], value_type)
		elif '.' in tokens_list[token_index]['content']:
			hasError(tokens_list[token_index], 'float')
		elif 'NRO' == tokens_list[token_index]['category']:
			hasError(tokens_list[token_index], 'int')
		else:
			hasError(tokens_list[token_index], 'boolean')
		next()
		return
	
	elif '(' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
		next()
		logicValue()
		#relationalExpression()
		if ')' == tokens_list[token_index]['content']:
			print(tokens_list[token_index]['content'], end=" ")
			next()
			return
	else :
		errorRecovery(tokens_list[token_index], follow_relacional_value)
		identify()

#***********************************************************************************************
# IDENTIFICADOR
#***********************************************************************************************
def identify():
	global tokens_list, token_index, result, identify_value

	print(tokens_list[token_index]['content'], end=" ")
	value =tokens_list[token_index]['content']
	result = search_declaration(tokens_list[token_index])
	next()
	if "[" == tokens_list[token_index]['content'] :
		matrix()
	elif tokens_list[token_index]['content'] in first_term_rest or tokens_list[token_index]['content'] in first_expression_rest:
		#chama expressao
		expression()
	elif "=" == tokens_list[token_index]['content']:
		#chama atribuicao
		assignment()
	elif tokens_list[token_index]['content'] in follow_relacional_value:
		#chama expressao relacional
		relationalExpression()
	elif tokens_list[token_index]['content'] in follow_logic_value:
		#chama expressao logica
		logicExpression()
	elif "(" == tokens_list[token_index]['content']:
		#chama chamada de funcao
		functionCall()
	elif "extends" == tokens_list[token_index]['content']:
		#chama extends
		Extends()
	elif "." == tokens_list[token_index]['content']:
		#chama tipo composto
		compType()
	else: # é apenas um valor (num ou var)
		identify_value = value
#***********************************************************************************************
# BLOCO
#***********************************************************************************************
def matchOpenBlock():
	if('{' == tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'])
		next()
		block()
		matchCloseCBrackets()
	else :
		error ="Erro: Símbolo inesperado na linha "+tokens_list[token_index]['line']+": "+tokens_list[token_index]['content']
		errorRecovery(error, ["PRE", "IDE"])
		block()
		matchCloseCBrackets()

def block():
	#print(tokens_list[token_index]['content'] )
	if tokens_list[token_index]['content'] in first_expression or tokens_list[token_index]['category'] in first_expression or tokens_list[token_index]['content'] in first_relational_expression or tokens_list[token_index]['category'] in first_relational_expression or tokens_list[token_index]['content'] in first_logic_expression or tokens_list[token_index]['category'] in first_logic_expression or tokens_list[token_index]['category'] in first_matrix or tokens_list[token_index]['category'] in  first_function_call:
		identify()
	elif tokens_list[token_index]['content'] == "print":
		Print()
	elif tokens_list[token_index]['content'] == "read":
		Read()
	elif tokens_list[token_index]['content'] == "while":
		While()
	elif tokens_list[token_index]['content'] == "if":
		If()
	elif tokens_list[token_index]['content'] == "var":
		Var()
	elif tokens_list[token_index]['content'] == "const":
		Const()
	if tokens_list[token_index]['content'] != "}" and tokens_list[token_index]['content'] !="return" and token_index<len(tokens_list)-1:
		if tokens_list[token_index]['content'] in first_block or tokens_list[token_index]['category'] in first_block:
			block()
		else :
			next()
			errorRecovery(tokens_list[token_index], ["}"]+first_block+first_start)
		

def matchCloseCBrackets():
	if('}' == tokens_list[token_index]['content']): #token que finaliza o bloco de declaração
		print(tokens_list[token_index]['content'])
		next()
	else: # se não encontrou '}' sinaliza o erro e continua o programa a partir de start()
		#error ="Erro: Símbolo inesperado na linha "+tokens_list[token_index]['line']+": "+tokens_list[token_index]['content']
		errorRecovery(tokens_list[token_index], first_start+first_block)

#***********************************************************************************************
# RECUPERAÇÃO DE ERROS
#***********************************************************************************************
def errorRecovery(token, followSet):
	error = "Erro: Símbolo inesperado na linha "+str(token['line'])+": "+str(token['content'])
	syntatic_errors_list.append(error)
	print("\n"+YEL+error+RESET)
	if followSet:
		while tokens_list[token_index]['content'] not in followSet:
			next()
			if token_index >= len(tokens_list)-1:
				break

def hasError(token, type):
	if not result[0] or not type[0]: 
		error = "Erro: Variável não declarada na linha "+str(result[1]['line'])
		semantic_errors_list.append(error)
		print("\n"+RED+error+RESET)
	elif type != result[0]:
		error = "Erro: Tipos incompatíveis na linha "+str(token['line'])+": "+str(type)+" e "+str(result[0])
		semantic_errors_list.append(error)
		print("\n"+RED+error+RESET)


#***********************************************************************************************
# PROXIMO TOKEN
#***********************************************************************************************
def next():
	global tokens_list, token_index
	if  token_index < len(tokens_list)-1:
		token_index +=1