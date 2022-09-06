class Token:
	@staticmethod
	def generate_token(token_type, content, line):
		type_list = [
			"STRING",
			"IDENTIFIER",
			"NUMBER",
			"LINE_COMMENT",
			"BLOCK_COMMENT",
			"SEMICOLON",
			"COMMA",
			"OPEN_PARENTHESES",
			"CLOSE_PARENTHESES",
			"OPEN_BRACKETS",
			"CLOSE_BRACKETS",
			"OPEN_CURLY_BRACES",
			"CLOSE_CURLY_BRACES",
			"DOT",
			"STRING_ERROR",
			"BLOCK_COMMENT_ERROR",
			"NUMBER_ERROR",
			"ARITHMETIC_ADDER",
			"ARITHMETIC_INCREMENT",
			"ARITHMETIC_DIVISOR",
			"ARITHMETIC_MULT",
			"ARITHMETIC_SUBTRACTOR",
			"ARITHMETIC_DECREMENT",
			"DIFFERENT",
			"EQUAL",
			"LESSER_THAN",
			"LESSER_EQUAL_THAN",
			"GREATER_THAN",
			"GREATER_EQUAL_THAN",
			"ASSINGMENT",
			"NOT",
			"AND",
			"OR",
			"INVALID_CHARACTER"
		]

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

		token_type = type_list[token_type]
		
		if token_type == 'IDENTIFIER':
			if(keywords.get(content)):
				token_type = keywords.get(content)

		token = {
			"line": str(line),
			"type": token_type,
			"content": content
		}

		return token

		#return "< "+ str(line) +" | "+ token_type +" | "+ content +" >"