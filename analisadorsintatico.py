from analisadorlexico import AnalisadorLexico
lookahead = 0
tokens_list = []
token_index = 0


#firstEstrutura = ["struct"]
#firstMatriz = ["IDE"]
#firstExpressao = ["IDE", "NRO", "("]
#firstPrint = ["print"]
#firstRead = ["read"]
#firstExpressaoRelacional = ["IDE", "NRO", "CAC", "(", "true", "false"]
#firstChamadaFuncao = ["IDE"]
#firstExpressaoLogica = ["!", "IDE", "NRO", "CAC", "(", "true", "false"]
#firstBloco = ["{"]
#firstWhile = ["while"]
#firstIf = ["if"]
#firstFuncao = ["function"]
#firstProcedimento = ["procedure"]
#firstDeclaracaoStruct = ["struct"]
#firstExtendstc = ["IDE"]
#firstVarDeclaracao = ["var"]
#firstConstantes = ["const"]
firstTermRest = ["*", "/"]
firstExpressionRest = ["+", "-"]
followRelacionalValue = [ '!=' , '==' , '<' , '<=' , '>' , '>=' , '=']
followLogicValue = [ '&&', '||']

# conjunto first:
#<Estrutura> = "struct"
#<Matriz>    = "IDE"
#<Expressao> = "IDE"  "NRO" "(" 
#<Print>    = "print"
#<Read>    = "read"
#<ExpressaoRelacional> = "IDE"  "NRO"  "CAC" "(" "true" "false"
#<ChamadaFuncao> = "IDE"
#<ExpressaoLogica> = "!" "IDE"  "NRO"  "CAC" "(" "true" "false"
# <Bloco> = "{"
# <While> = "while"
# <If> = "if"
# <Funcao> = "function"
# <Procedimento> = "procedure"
# <DeclaracaoStruct> = "struct"
# <Extendstc> = "IDE"
# <VarDeclaracao> = "var"
# <Constantes> = "const"
def start():
    global tokens_list, token_index
    print("Start ...") 
    
    if token_index < len(tokens_list)-1:
        #print(tokens_list[token_index]['content'])
        if tokens_list[token_index]['content'] == "struct":
            pass
        elif tokens_list[token_index]['content'] == "read": 
            Read()
        elif tokens_list[token_index]['content'] == "print": 
            Print()
        elif tokens_list[token_index]['content'] == "true": 
            pass
        elif tokens_list[token_index]['content'] == "false": 
            pass
        elif tokens_list[token_index]['content'] == "while": 
            While()
        elif tokens_list[token_index]['content'] == "if": 
            pass
        elif tokens_list[token_index]['content'] == "function": 
            pass
        elif tokens_list[token_index]['content'] == "procedure": 
            pass
        elif tokens_list[token_index]['content'] == "var": 
            pass
        elif tokens_list[token_index]['content'] == "const": 
            pass
        elif tokens_list[token_index]['content'] == "!": 
            logicExpression()
            start()
        elif tokens_list[token_index]['content'] == "(": 
            pass
        elif tokens_list[token_index]['content'] == "{": 
            pass
        elif tokens_list[token_index]['category'] == "IDE":
            identify()
            start()
        elif tokens_list[token_index]['category'] == "NRO":
            number()
            start()
        elif tokens_list[token_index]['category'] == "CAC":
            pass

#***********************************************************************************************
# STRUCT
#***********************************************************************************************
def Struct():
    pass

#***********************************************************************************************
# READ
#***********************************************************************************************
def Read(): 
    global tokens_list, token_index
    
    if('read'== tokens_list[token_index]['content']):
        token_index += 1
        if('(' == tokens_list[token_index]['content']):
            token_index += 1
            #tratar conteudo
            print(tokens_list[token_index]['content'])
            token_index += 1
            if(')' == tokens_list[token_index]['content']):
                token_index += 1
                if(';' == tokens_list[token_index]['content']):
                    print("Read ok")
                else:
                    hasError = True
                    print("Erro:linha "+tokens_list[token_index]['line']+" - Esperava \";\"")
            else:
                hasError = True
                print("Linha "+tokens_list[token_index]['line']+" - Esperava \")\"")
        else:
            hasError = True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"(\"")
    else:
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"read\"")
    
    next()
    start()


#***********************************************************************************************
# PRINT
#***********************************************************************************************
def Print(): 
    global tokens_list, token_index

    if('print'== tokens_list[token_index]['content']):
        token_index += 1
        if('(' == tokens_list[token_index]['content']):
            token_index += 1
            #tratar conteudo 
            print(tokens_list[token_index]['content'])
            token_index += 1
            if(')' == tokens_list[token_index]['content']):
                token_index += 1
                if(';' == tokens_list[token_index]['content']):
                    print("Print ok")
                else:
                    hasError = True
                    print("Linha "+tokens_list[token_index]['line']+" - Esperava \";\"")
            else:
                hasError = True
                print("Linha "+tokens_list[token_index]['line']+" - Esperava \")\"")
        else:
            hasError = True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"(\"")
    else:
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"print\"")
    next()
    start()

#***********************************************************************************************
# WHILE
#***********************************************************************************************
def While(): 
    global tokens_list, token_index

    if('while'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('(' == tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            #tratar expressao
            identify()
            print(tokens_list[token_index]['content'])
            next()
            if(')' == tokens_list[token_index]['content']):
                next()
                if('{' == tokens_list[token_index]['content']):
                    print("Entrou while")
                    #tratar bloco
            else :
                hasError = True
        else:
            hasError=True
    else :
        hasError=True

#***********************************************************************************************
# NUMERO
#***********************************************************************************************
def number():
    global tokens_list, token_index
    number = tokens_list[token_index]['content']
    print(tokens_list[token_index]['content'])
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
        print(tokens_list[token_index]['content'])
        next()
        factor()
        term()
        if '+' == tokens_list[token_index]['content'] or '-' == tokens_list[token_index]['content'] and token_index<len(tokens_list)-1:
            print(tokens_list[token_index]['content'])
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
        print(tokens_list[token_index]['content'])
        next()
        factor()
        if '*' == tokens_list[token_index]['content'] or '/' == tokens_list[token_index]['content'] and token_index<len(tokens_list):
            print(tokens_list[token_index]['content'])
            next()
            factor()
        else :
            return

def factor():
    global tokens_list, token_index
    
    if 'IDE' == tokens_list[token_index]['category'] or 'NRO' == tokens_list[token_index]['category'] and token_index<len(tokens_list):
        print(tokens_list[token_index]['content'])
        next()
        return
    elif '(' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        factor()
        expression()
        if ')' == tokens_list[token_index]['content']:
            print(tokens_list[token_index]['content'])
            next()
            return
    else :
        print("Erro")
    

#***********************************************************************************************
#EXPRESSÃO LÓGICA
#***********************************************************************************************
def logicExpression():
    global tokens_list, token_index

    if '!' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        logicValue()
    else :
        #logicValue()
        logicOperator()

def logicOperator():
    global tokens_list, token_index
    
    if '&&' == tokens_list[token_index]['content'] or '||' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        logicValue()
        if '&&' == tokens_list[token_index]['content'] or '||' == tokens_list[token_index]['content']:
            print(tokens_list[token_index]['content'])
            next()
            logicValue()

def logicValue():
    global tokens_list, token_index
    
    if 'IDE' == tokens_list[token_index]['category'] or 'true' == tokens_list[token_index]['content'] or  'true' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        return
    elif '(' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        logicValue()
        logicExpression()
        if ')' == tokens_list[token_index]['content']:
            print(tokens_list[token_index]['content'])
            next()
            return
    else :
        print("Erro")

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
    if tokens_list[token_index]['content'] in followRelacionalValue:
        print(tokens_list[token_index]['content'])
        next()
        relationalValue()
        if tokens_list[token_index]['content'] in followRelacionalValue:
            print(tokens_list[token_index]['content'])
            next()
            relationalValue()

def relationalValue():
    global tokens_list, token_index
    #print("$",tokens_list[token_index]['content'])
    if 'IDE' == tokens_list[token_index]['category'] or 'NRO' == tokens_list[token_index]['category'] or 'true' == tokens_list[token_index]['content'] or  'false' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        return
    
    elif '(' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        logicValue()
        #relationalExpression()
        if ')' == tokens_list[token_index]['content']:
            print(tokens_list[token_index]['content'])
            next()
            return
    else :
        print("Erro")

#***********************************************************************************************
# IDENTIFICADOR
#***********************************************************************************************
def identify():
    global tokens_list, token_index
    #<Matriz>    = "IDE"
    #<Expressao> = "IDE"  "NRO" "(" 
    #<ExpressaoRelacional> = "IDE"  "NRO"  "CAC" "(" "true" "false"
    #<ChamadaFuncao> = "IDE"
    #<ExpressaoLogica> = "!" "IDE"  "NRO"  "CAC" "(" "true" "false"
    #<Extendstc> = "IDE"
    print(tokens_list[token_index]['content'])
    next()
    if "[" == tokens_list[token_index]['content'] :
        #chama matriz
        pass
    elif tokens_list[token_index]['content'] in firstTermRest or tokens_list[token_index]['content'] in firstExpressionRest:
        #chama expressao
        expression()
    elif tokens_list[token_index]['content'] in followRelacionalValue:
        #chama expressao relacional
        relationalExpression()
    elif tokens_list[token_index]['content'] in followLogicValue:
        #chama expressao logica
        logicExpression()
    elif "(" == tokens_list[token_index]['content']:
        #chama chamada de funcao
        pass
    elif "extends" == tokens_list[token_index]['content']:
        #chama extends
        pass

#***********************************************************************************************
# PROXIMO TOKEN
#***********************************************************************************************
def next():
    global tokens_list, token_index
    if  token_index < len(tokens_list)-1:
        token_index +=1


def run():
    global tokens_list
    analisadorlexico = AnalisadorLexico()
    lists = analisadorlexico.run()
    for list in lists:
        #file = list["file"]
        tokens_list =list["tokens"]
        start()

# main
run()