from tokentype import keywords

''' Class Token - Used to generate tokens '''
class Token:
	@staticmethod
	def generate_token(token_type, content, line):
		token_type = token_type.name
		
		# If it's a identifier check the keyword dictionary 
		if token_type == 'IDENTIFIER':
			if(keywords.get(content)):
				token_type = keywords.get(content)

		token = {
			"line": str(line),
			"type": token_type,
			"content": content
		}

		return token