RED   = "\033[1;31m"  
RESET = "\033[0;0m"
tokens_list = []
token_index = 0
errors_list = []
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

class Processor:
	def __init__(self):
		self.tokens_list = []
		self.token_index = 0
		#self.errors_list = []

	def errors_list(self):
		global errors_list
		return errors_list
	
	def reset(self):
		global tokens_list, errors_list, token_index, start_procedure_flag
		tokens_list = []
		token_index = 0
		errors_list = []
		start_procedure_flag = False

	def process_tokens(self, tokens):
		global tokens_list
		tokens_list=tokens
		start()

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
	if('{' == tokens_list[token_index]['content']): #verifica se o token atual é '{'
		print(tokens_list[token_index]['content'])
		next()
	else: # se o token não for '{'
		errorRecovery(tokens_list[token_index], first_type) #imprime o erro e vai para o seguinte de '{' que é ['int','real','boolean','string', "IDE"]
	allVars() #continual chamando a funçao que analisa a declaracao das variaveis
	matchCloseCBrackets()

def allVars():
	if tokens_list[token_index]['content'] in first_type or tokens_list[token_index]['category'] in first_type: # verifica se o token é um tipo ['int','real','boolean','string', "IDE"]
		print(tokens_list[token_index]['content'], end=" ")
		next()
		varList() # funcao que verifica as variaveis declaradas
	else : #se o token não for um tipo
		errorRecovery(tokens_list[token_index], first_type+[";"])  #imprime o erro e vai para o seguinte do tipo que pode ser outros tipos ou ';' 
		allVars()#continual chamando a funçao que analisa a declaracao das variaveis

def varList():
	if tokens_list[token_index]['category'] == "IDE": # se o token é um identificador
		print(tokens_list[token_index]['content'], end=" ")
		next()
		varListSeparation() # funcao que analisa atribuicao ou lista de variáveis: a=10, b, i=0 
		commaSeparation()
		"""if tokens_list[token_index]['content'] == ",": #se o proximo token for ','
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
					errorRecovery(tokens_list[token_index], ["}"]+ first_type)
					if tokens_list[token_index]['content'] in first_type or tokens_list[token_index]['category'] in first_type: #se o token for um tipo
						allVars() # chama funcao que trata as declaracões"""
	else : #se o token não for um identificador
		errorRecovery(tokens_list[token_index], [";", ","])
		commaSeparation() # funcao que analisa atribuicao ou lista de variaveis: a=10, b, i=0

def  commaSeparation():
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
	if tokens_list[token_index]['content'] == "=": # se token for o operador de atribuiçao
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if tokens_list[token_index]['category'] == "NRO": # verifica se é um número
			number()
		elif tokens_list[token_index]['category'] == "CAC":
			print(tokens_list[token_index]['content'], end=" ")
			next()
		else : # se não for numero é identificador
			identify()
		
def assignment():
	if tokens_list[token_index]['content'] == "=": # se o token for operador de atribuiçao
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if tokens_list[token_index]['category'] == "NRO":
			number()
		elif tokens_list[token_index]['category'] == "CAC":
			print(tokens_list[token_index]['content'], end=" ")
			next()
		elif tokens_list[token_index]['category'] == "IDE":
			identify()
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
	identify()
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
	if('function'== tokens_list[token_index]['content']):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if(tokens_list[token_index]['content'] in first_type): # verifica se o token é um tipo
			print(tokens_list[token_index]['content'], end=" ")
			next()
			functionName() 
		else :
			errorRecovery(tokens_list[token_index], ["IDE", "("])
			functionName()
	else :
		errorRecovery(tokens_list[token_index], [])

def functionName():
	if('IDE' == tokens_list[token_index]['category']): #verifica se o token é um identificador
		print(tokens_list[token_index]['content'], end=" ")
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
	if(tokens_list[token_index]['content'] in first_type):
		print(tokens_list[token_index]['content'], end=" ")
		next()
		if('IDE'== tokens_list[token_index]['category']):
			print(tokens_list[token_index]['content'], end=" ")
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
	global tokens_list, token_index
	
	if 'IDE' == tokens_list[token_index]['category'] or 'true' == tokens_list[token_index]['content'] or  'true' == tokens_list[token_index]['content']:
		print(tokens_list[token_index]['content'], end=" ")
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
	global tokens_list, token_index

	print(tokens_list[token_index]['content'], end=" ")
	next()
	if "[" == tokens_list[token_index]['content'] :
		#chama matriz
		matrix()
	elif tokens_list[token_index]['content'] in first_term_rest or tokens_list[token_index]['content'] in first_expression_rest:
		#chama expressao
		expression()
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
	elif "=" == tokens_list[token_index]['content']:
		#chama atribuicao
		assignment()
	elif "." == tokens_list[token_index]['content']:
		#chama tipo composto
		compType()

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
	errors_list.append(error)
	print("\n"+RED+error+RESET)
	if followSet:
		while tokens_list[token_index]['content'] not in followSet:
			next()
			if token_index >= len(tokens_list)-1:
				break

#***********************************************************************************************
# PROXIMO TOKEN
#***********************************************************************************************
def next():
	global tokens_list, token_index
	if  token_index < len(tokens_list)-1:
		token_index +=1