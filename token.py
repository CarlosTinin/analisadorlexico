from tokentype import keywords

''' Class Token - Used to generate tokens '''
class Token:
	@staticmethod
	def generate_token(token_type, content, line):		
		token_type = token_type.name
		type_dict = {
			"STRING": "CAC",
			"IDENTIFIER": "IDE",
			"NUMBER": "NRO",
			"LINE_COMMENT": "LCO",
			"BLOCK_COMMENT": "BCO",
			"SEMICOLON": "DEL",
			"COMMA": "DEL",
			"OPEN_PARENTHESES": "DEL",
			"CLOSE_PARENTHESES": "DEL",
			"OPEN_BRACKETS": "DEL",
			"CLOSE_BRACKETS": "DEL",
			"OPEN_CURLY_BRACES": "DEL",
			"CLOSE_CURLY_BRACES": "DEL",
			"DOT": "DEL",
			"STRING_ERROR": "CMF",
			"BLOCK_COMMENT_ERROR": "CoMF",
			"NUMBER_ERROR": "NMF",
			"ARITHMETIC_ADDER": "ART",
			"ARITHMETIC_INCREMENT": "ART",
			"ARITHMETIC_DIVISOR": "ART",
			"ARITHMETIC_MULT": "ART",
			"ARITHMETIC_SUBTRACTOR": "ART",
			"ARITHMETIC_DECREMENT": "ART",
			"DIFFERENT": "REL",
			"EQUAL": "REL",
			"LESSER_THAN": "REL",
			"LESSER_EQUAL_THAN": "REL",
			"GREATER_THAN": "REL",
			"GREATER_EQUAL_THAN": "REL",
			"ASSINGMENT": "REL",
			"NOT": "LOG",
			"AND": "LOG",
			"OR": "LOG",
			"INVALID_CHARACTER": "TMF"
		}

		keywords = {
			"var": "VAR",
			"const": "CONST",
			"struct": "STRUCT",
			"extends": "EXTENDS",
			"procedure": "PROCEDURE",
			"function": "FUNCTION",
			"start": "START",
			"return": "RETURN",
			"if": "IF",
			"else": "ELSE",
			"then": "THEN",
			"while": "WHILE",
			"read": "READ",
			"print": "PRINT",
			"int": "INT",
			"real": "REAL",
			"boolean": "BOOLEAN",
			"string": "STRING",
			"true": "TRUE",
			"false": "FALSE",
		}

		token_category = type_dict.get(token_type)

		if token_type == 'IDENTIFIER':
			if(keywords.get(content)):
				token_type = keywords.get(content)
				token_category ="PRE"

		token = {
			"line": str(line),
			"type": token_type,
			"content": content,
			"category": token_category
		}

		return token