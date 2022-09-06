class Token:
	@staticmethod
	def generate_token(token_id, token_type, content):
		type_list = [
			"STRING",
			"IDENTIFIER",
			"NUMBER",
			"LINE_COMMENT",
			"BLOCK_COMMENT",
			";",
			",",
			"(",
			")",
			"[",
			"]",
			"{",
			"}",
			".",
			"STRING_ERROR",
			"BLOCK_COMMENT_ERROR",
			"NUMBER_ERROR"
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

		return "< "+ str(token_id) +" | "+ token_type +" | "+ content +" >"