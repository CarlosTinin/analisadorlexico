from analisadorlexico import AnalisadorLexico
tokens_list = []
token_index = 0


#firstEstrutura = ["struct"]
firstMatrix = ["IDE"]
firstExpression = ["IDE", "NRO", "("]
#firstPrint = ["print"]
#firstRead = ["read"]
firstRelationalExpression = ["IDE", "NRO", "CAC", "(", "true", "false"]
firstFunctionCall = ["IDE"]
firstLogicExpression = ["!", "IDE", "NRO", "CAC", "(", "true", "false"]
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
firstType = ['int','real','boolean','string', "IDE"]
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
        print(tokens_list[token_index]['content'])
        if tokens_list[token_index]['content'] == "struct":
            pass
        elif tokens_list[token_index]['content'] == "read": 
            Read()
            start()
        elif tokens_list[token_index]['content'] == "print": 
            Print()
            start()
        elif tokens_list[token_index]['content'] == "true": 
            pass
        elif tokens_list[token_index]['content'] == "false": 
            pass
        elif tokens_list[token_index]['content'] == "while": 
            While()
            start()
        elif tokens_list[token_index]['content'] == "if": 
            If()
            start()
        elif tokens_list[token_index]['content'] == "function": 
            function()
            start()
        elif tokens_list[token_index]['content'] == "procedure": 
            procedure()
            start()
        elif tokens_list[token_index]['content'] == "var": 
            Var()
            start()
        elif tokens_list[token_index]['content'] == "const": 
            Const()
            start()
        elif tokens_list[token_index]['content'] == "!": 
            logicExpression()
            start()
        elif tokens_list[token_index]['content'] == "(": 
            identify()
            start()
        elif tokens_list[token_index]['content'] == "{": 
            block()
            start()
        elif tokens_list[token_index]['category'] == "IDE":
            identify()
            start()
        elif tokens_list[token_index]['category'] == "NRO":
            number()
            start()
        elif tokens_list[token_index]['category'] == "CAC":
            pass


#***********************************************************************************************
# CONST 
#***********************************************************************************************
def Const():
    if('const'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('{' == tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            allVars()
            if('}' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
            else:
                hasError = True
                print("Linha "+tokens_list[token_index]['line']+" - Esperava \"}\"")
        else:
            hasError = True
            print("Linha "+tokens_list[token_index]['line']+" - Esperava \"{\"")
    else:
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"const\"")

#***********************************************************************************************
# VAR 
#***********************************************************************************************
def Var():
    if('var'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('{' == tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            allVars()
            if('}' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
            else:
                hasError = True
                print("Linha "+tokens_list[token_index]['line']+" - Esperava \"}\"")
        else:
            hasError = True
            print("Linha "+tokens_list[token_index]['line']+" - Esperava \"{\"")
    else:
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"var\"")
    #next()

def allVars():
    if tokens_list[token_index]['content'] in firstType or tokens_list[token_index]['category'] in firstType:
        print(tokens_list[token_index]['content'])
        next()
        varList()
        if tokens_list[token_index]['content'] == ";":
            print(tokens_list[token_index]['content'])
            next()
            if tokens_list[token_index]['content'] in firstType or tokens_list[token_index]['category'] in firstType:
                #print(tokens_list[token_index]['content'])
                allVars()

def varList():
    if tokens_list[token_index]['category'] in firstType:
        print(tokens_list[token_index]['content'])
        next()
        if tokens_list[token_index]['content'] == "=":
            print(tokens_list[token_index]['content'])
            next()
            identify()
        else :
            if tokens_list[token_index]['content'] == ",":
                print(tokens_list[token_index]['content'])
                next()
                varList()

def assignment():
    if tokens_list[token_index]['content'] == "=":
        print(tokens_list[token_index]['content'])
        next()
        print("¨¨¨¨¨¨", tokens_list[token_index]['content'])
        identify()

#***********************************************************************************************
# MATRIZ
#***********************************************************************************************
def matrix():
    access()
    if('['== tokens_list[token_index]['content']):
        access()

def access():
    if('['== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        identify()
        if(']'== tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
        else :
            hasError=True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"]\"")
    else:
        hasError=True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"[\"")

#***********************************************************************************************
# STRUCT
#***********************************************************************************************
def Struct():
    pass

def StructDeclaration():
    global tokens_list, token_index

    if('struct'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('IDE' == tokens_list[token_index]['category']):
            print(tokens_list[token_index]['content'])
            next()
            if('{' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                allVars()
                if('}' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
                else:
                    hasError = True
                    print("Linha "+tokens_list[token_index]['line']+" - Esperava \"}\"")
            else:
                hasError = True
                print("Linha "+tokens_list[token_index]['line']+" - Esperava \")\"")
        else:
            hasError = True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"IDE\"")
    else:
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"struct\"")


def compType():
    if('.' == tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('IDE' == tokens_list[token_index]['category']):
            print(tokens_list[token_index]['content'])
            next()
    else :
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \".\"")

#***********************************************************************************************
# EXTENDS
#***********************************************************************************************
def Extends():
    global tokens_list, token_index
    if('extends'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('IDE' == tokens_list[token_index]['category']):
            print(tokens_list[token_index]['content'])
            next()
            if('{' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                allVars()
                if('}' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
                else:
                    hasError = True
                    print("Linha "+tokens_list[token_index]['line']+" - Esperava \"}\"")
            else:
                hasError = True
                print("Linha "+tokens_list[token_index]['line']+" - Esperava \")\"")
        else:
            hasError = True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"IDE\"")
    else:
        hasError = True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"struct\"")
        

#***********************************************************************************************
# READ
#***********************************************************************************************
def Read(): 
    global tokens_list, token_index
    
    if('read'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('(' == tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            #tratar conteudo
            print(tokens_list[token_index]['content'])
            token_index += 1
            if(')' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                if(';' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
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

def reading():
    pass

#***********************************************************************************************
# PRINT
#***********************************************************************************************
def Print(): 
    global tokens_list, token_index

    if('print'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('(' == tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            #tratar conteudo 
            print(tokens_list[token_index]['content'])
            token_index += 1
            if(')' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                if(';' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
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
    #next()

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
            if(')' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                if('{' == tokens_list[token_index]['content']):
                    print("Entrou while")
                    print(tokens_list[token_index]['content'])
                    next()
                    block()
                    if('}' == tokens_list[token_index]['content']):
                        print(tokens_list[token_index]['content'])
                        next()
                    else:
                        hasError=True
                        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"}\"")
                else :
                    hasError = True
                    print("Linha"+tokens_list[token_index]['line']+" - Esperava \"{\"")
            else :
                hasError = True
                print("Linha"+tokens_list[token_index]['line']+" - Esperava \")\"")
        else:
            hasError=True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"(\"")
    else :
        hasError=True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"while\"")


#***********************************************************************************************
# IF
#***********************************************************************************************
def If():
    if('if'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('(' == tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            #tratar expressao
            identify()
            if(')' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                if('then' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
                    if('{' == tokens_list[token_index]['content']):
                        print("Entrou if")
                        print(tokens_list[token_index]['content'])
                        next()
                        block()
                        if('}' == tokens_list[token_index]['content']):
                            print(tokens_list[token_index]['content'])
                            next()
                        else:
                            hasError=True
                            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"}\"")
                        if('else' == tokens_list[token_index]['content']):
                            print(tokens_list[token_index]['content'])
                            next()
                            if('{' == tokens_list[token_index]['content']):
                                print("Entrou if")
                                print(tokens_list[token_index]['content'])
                                next()
                                block()
                                if('}' == tokens_list[token_index]['content']):
                                    print(tokens_list[token_index]['content'])
                                    next()
                                else:
                                    hasError=True
                                    print("Linha"+tokens_list[token_index]['line']+" - Esperava \"}\"")
                    else:
                        hasError = True
                        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"{\"")
                else :
                    hasError =True
                    print("Linha"+tokens_list[token_index]['line']+" - Esperava \"then\"")
            else :
                hasError = True
                print("Linha"+tokens_list[token_index]['line']+" - Esperava \")\"")
        else:
            hasError=True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"(\"")
    else :
        hasError=True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"if\"")

#***********************************************************************************************
# FUNCTION
#***********************************************************************************************
def function():
    if('function'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if(tokens_list[token_index]['content'] in firstType):
            print(tokens_list[token_index]['content'])
            next()
            if('IDE' == tokens_list[token_index]['category']):
                print(tokens_list[token_index]['content'])
                next()
                if('(' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
                    paramList()
                    if(')' == tokens_list[token_index]['content']):
                        print(tokens_list[token_index]['content'])
                        next()
                        if('{' == tokens_list[token_index]['content']):
                            print(tokens_list[token_index]['content'])
                            next()
                            block()
                            if('return' == tokens_list[token_index]['content']):
                                print(tokens_list[token_index]['content'])
                                next()
                                identify()
                                if(';' == tokens_list[token_index]['content']):
                                    print(tokens_list[token_index]['content'])
                                    next() 
                                    if('}' == tokens_list[token_index]['content']):
                                        print(tokens_list[token_index]['content'])
                                        next()
                                    else :
                                        hasError=True
                                        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"}\"")
                                else :
                                    hasError=True
                                    print("Linha"+tokens_list[token_index]['line']+" - Esperava \";\"")
                            else :
                                hasError=True
                                print("Linha"+tokens_list[token_index]['line']+" - Esperava \"return\"")
                        else :
                            hasError=True
                            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"{\"")
                    else:
                        hasError=True
                        print("Linha"+tokens_list[token_index]['line']+" - Esperava \")\"")
                else:
                    hasError=True
                    print("Linha"+tokens_list[token_index]['line']+" - Esperava \"(\"")
            else :
                hasError=True
                print("Linha"+tokens_list[token_index]['line']+" - Esperava \"variavel\"")

        else :
            hasError = True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"tipo\"")
    else :
        hasError=True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"procedure\"")


def paramList():
    if(tokens_list[token_index]['content'] in firstType):
        print(tokens_list[token_index]['content'])
        next()
        if('IDE'== tokens_list[token_index]['category']):
            print(tokens_list[token_index]['content'])
            next()
            if(','== tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                paramList()

def parameters():
    if 'IDE' == tokens_list[token_index]['category'] :
        print(tokens_list[token_index]['content'])
        next()
        if '[' == tokens_list[token_index]['content']:
            matrix()
        elif '.' == tokens_list[token_index]['content']:
            compType()
        elif '(' == tokens_list[token_index]['content']:
            functionCall()
    elif 'NRO' == tokens_list[token_index]['category'] or 'CAC' == tokens_list[token_index]['category']:
        print(tokens_list[token_index]['content'])
        next()
    
    if ',' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        parameters()
        pass

def functionCall():
    if'(' == tokens_list[token_index]['content']:
        print(tokens_list[token_index]['content'])
        next()
        parameters()
        if')' == tokens_list[token_index]['content']:
            print(tokens_list[token_index]['content'])
            next()
            if';' == tokens_list[token_index]['content']:
                print(tokens_list[token_index]['content'])
                next()

#***********************************************************************************************
# PROCEDURE
#***********************************************************************************************
def procedure():
    if('procedure'== tokens_list[token_index]['content']):
        print(tokens_list[token_index]['content'])
        next()
        if('IDE' == tokens_list[token_index]['category'] or 'start'== tokens_list[token_index]['content']):
            print(tokens_list[token_index]['content'])
            next()
            if('(' == tokens_list[token_index]['content']):
                print(tokens_list[token_index]['content'])
                next()
                paramList()
                if(')' == tokens_list[token_index]['content']):
                    print(tokens_list[token_index]['content'])
                    next()
                    if('{' == tokens_list[token_index]['content']):
                        print(tokens_list[token_index]['content'])
                        next()
                        block()
                        if('}' == tokens_list[token_index]['content']):
                            print(tokens_list[token_index]['content'])
                            next()
                        else:
                            hasError=True
                            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"}\"")
                    else :
                        hasError=True
                        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"{\"")
                else:
                    hasError=True
                    print("Linha"+tokens_list[token_index]['line']+" - Esperava \")\"")
            else:
                hasError=True
                print("Linha"+tokens_list[token_index]['line']+" - Esperava \"(\"")
        else :
            hasError=True
            print("Linha"+tokens_list[token_index]['line']+" - Esperava \"variavel\"")
    else :
        hasError=True
        print("Linha"+tokens_list[token_index]['line']+" - Esperava \"procedure\"")


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
        matrix()
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
def block():
    print("entrou bloco ",tokens_list[token_index]['content'] )
    if tokens_list[token_index]['content'] in firstExpression or tokens_list[token_index]['category'] in firstExpression or tokens_list[token_index]['content'] in firstRelationalExpression or tokens_list[token_index]['category'] in firstRelationalExpression or tokens_list[token_index]['content'] in firstLogicExpression or tokens_list[token_index]['category'] in firstLogicExpression or tokens_list[token_index]['category'] in firstMatrix or tokens_list[token_index]['category'] in  firstFunctionCall:
        identify()
    elif tokens_list[token_index]['content'] == "print":
        Print()
    elif tokens_list[token_index]['content'] == "read":
        Read()
    elif tokens_list[token_index]['content'] == "while":
        print(tokens_list[token_index]['content'])
        While()
    elif tokens_list[token_index]['content'] == "if":
        If()
    elif tokens_list[token_index]['content'] == "var":
        Var()
    elif tokens_list[token_index]['content'] == "const":
        Const()
    
    if tokens_list[token_index]['content'] != "}" and tokens_list[token_index]['content'] !="return":
        block()

        
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