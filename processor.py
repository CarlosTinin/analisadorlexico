from tokentype import TokenType
from token import Token
import re

class Processor:
	def __init__(self):
		self.token_list = []
		self.state = 0
		self.line_accumulator = ''

	def process_file(self, file):
		for line_key, line in enumerate(file.readlines()):
			for char in line:
				self.process_character(char, line_key)
		else:
			if (self.state ==  13):
				self.store_token_and_reset(TokenType.BLOCK_COMMENT_ERROR, line_key)

	def process_character(self, char, line_key):
		match self.state:
			case 0:
				if(re.match(r'[A-Z]|[a-z]', char)):
					self.line_accumulator += char
					self.state = 1
				elif(re.match(r'[0-9]', char)):
					self.line_accumulator += char
					self.state = 2
				elif(char == "+"):
					self.line_accumulator += char
					self.state = 3
				elif(char == "*"):				
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.ARITHMETIC_MULT, line_key)
				elif(char == "-"):
					self.line_accumulator += char
					self.state = 4
				elif(char == "&"):
					self.line_accumulator += char
					self.state = 16
				elif(char == "|"):
					self.line_accumulator += char
					self.state = 17
				elif(char == "!"):
					self.line_accumulator += char
					self.state = 5
				elif(char == "="):
					self.line_accumulator += char
					self.state = 8
				elif(char == ">"):
					self.line_accumulator += char
					self.state = 9
				elif(char == "<"):
					self.line_accumulator += char
					self.state = 10
				elif(char == '"'):
					self.line_accumulator += char
					self.state = 15
				elif(char == '/'):
					self.line_accumulator += char
					self.state = 11
				elif(char == ';'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.SEMICOLON, line_key)
				elif(char == ','):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.COMMA, line_key)
				elif(char == '('):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.OPEN_PARENTHESES, line_key)
				elif(char == ')'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.CLOSE_PARENTHESES, line_key)
				elif(char == '['):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.OPEN_BRACKETS, line_key)
				elif(char == ']'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.CLOSE_BRACKETS, line_key)
				elif(char == '{'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.OPEN_CURLY_BRACES, line_key)
				elif(char == '}'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.CLOSE_CURLY_BRACES, line_key)
				elif(char == '.'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.DOT, line_key)
				else:
					if(char != " " and char != "\t" and char != "\n"):
						self.line_accumulator += char
						self.store_token_and_reset(TokenType.INVALID_CHARACTER, line_key)

			case 1:
				if(re.match(r'[A-Z]|[a-z]', char) or re.match(r'[0-9]', char) or (char == '_')):
					self.line_accumulator += char
				else:
					self.store_token_and_reset(TokenType.IDENTIFIER, line_key)
					self.process_character(char, line_key)

			case 2:
				if(re.match(r'[0-9]', char)):
					self.line_accumulator += char
				elif(char == '.'):
					self.line_accumulator += char
					self.state = 6
				else:
					self.store_token_and_reset(TokenType.NUMBER, line_key)
					self.process_character(char, line_key)

			case 3:
				if(char == "+"):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.ARITHMETIC_INCREMENT, line_key)
				else: #this store a +
					self.store_token_and_reset(TokenType.ARITHMETIC_ADDER, line_key)
					self.process_character(char, line_key)
			case 4:
				if(char == "-"): # this store a --
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.ARITHMETIC_DECREMENT, line_key)
				elif(re.match(r'[0-9]', char)): # checks if is - followed by number
					self.line_accumulator += char
					self.state = 2
				elif(re.match(r'[A-Z]|[a-z]', char)):  # checks if is - followed by letter
					self.store_token_and_reset(TokenType.ARITHMETIC_SUBTRACTOR, line_key)
					self.line_accumulator += char
					self.state = 1
				else:
					if(char != " "):# checks if is a space
						self.line_accumulator += char
					self.state = 18
			case 5:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.DIFFERENT, line_key)
				else:
					self.store_token_and_reset(TokenType.NOT, line_key)
					self.process_character(char, line_key)

			case 6:
				if(re.match(r'[0-9]', char)):
					self.line_accumulator += char
					self.state = 7
				else:
					self.store_token_and_reset(TokenType.NUMBER_ERROR, line_key)
					self.process_character(char, line_key)

			case 7:
				if(re.match(r'[0-9]', char)):
					self.line_accumulator += char
				else:
					self.store_token_and_reset(TokenType.NUMBER, line_key)
					self.process_character(char, line_key)

			case 8:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.EQUAL, line_key)
				else:
					self.store_token_and_reset(TokenType.ASSINGMENT, line_key)
					self.process_character(char, line_key)

			case 9:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.GREATER_EQUAL_THAN, line_key)
				else:
					self.store_token_and_reset(TokenType.GREATER_THAN, line_key)
					self.process_character(char, line_key)

			case 10:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.LESSER_EQUAL_THAN, line_key)
				else:
					self.store_token_and_reset(TokenType.LESSER_THAN, line_key)
					self.process_character(char, line_key)

			case 11:
				if(char == '/'):
					self.line_accumulator += char
					self.state = 12
				elif(char == '*'):
					self.line_accumulator += char
					self.state = 13
				else:
					self.store_token_and_reset(TokenType.ARITHMETIC_DIVISOR, line_key)
					self.process_character(char, line_key)

			case 12:
				if(char == "\n"):
					self.store_token_and_reset(TokenType.LINE_COMMENT, line_key)
				else:
					self.line_accumulator += char

			case 13:
				self.line_accumulator += char
				if(char == '*'):
					self.state = 14

			case 14:
				self.line_accumulator += char
				if(char == '/'):
					self.store_token_and_reset(TokenType.BLOCK_COMMENT, line_key)
				else:
					self.state = 13
					
			case 15: # this is a string
				#self.line_accumulator += char
				if(char == '"'):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.STRING, line_key)
				elif(char == '\n'):
					self.store_token_and_reset(TokenType.STRING_ERROR, line_key)
				else:
					self.line_accumulator += char

			case 16:
				if (char == "&"):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.AND, line_key)
				else:
					self.store_token_and_reset(TokenType.INVALID_CHARACTER, line_key)
					self.process_character(char, line_key)

			case 17:
				if (char == "|"):
					self.line_accumulator += char
					self.store_token_and_reset(TokenType.OR, line_key)
				else:
					self.store_token_and_reset(TokenType.INVALID_CHARACTER, line_key)
					self.process_character(char, line_key)

			case 18: 
				if(self.token_list[-1]['type'] =="NUMBER" or self.token_list[-1]['type'] =="IDENTIFIER"):# checks if the last token was a number or identifier
					self.store_token_and_reset(TokenType.ARITHMETIC_SUBTRACTOR, line_key)
					self.process_character(char, line_key)
				elif(re.match(r'[0-9]', char)): # checks if after the space there is a number
					self.line_accumulator += char
					self.state = 2
				elif(re.match(r'[A-Z]|[a-z]', char)):# checks if after the space there is a number
					self.line_accumulator += char
					self.state = 1
				elif(char == " "): 
					self.state = 18
				else: #stores a aritmetic operator
					self.store_token_and_reset(TokenType.ARITHMETIC_SUBTRACTOR, line_key)
					self.process_character(char, line_key)

	def show_token_list(self):
		return self.token_list;

	def store_token_and_reset(self, token_type, line):
		self.token_list.append(Token.generate_token(token_type, self.line_accumulator, line + 1))
		self.state = 0
		self.line_accumulator = ''