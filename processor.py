import token
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
				self.store_token_and_reset(15, line_key)

	def process_character(self, char, line_key):
		match self.state:
			case 0:
				if(re.match(r'[A-Z]|[a-z]', char)): # this is a identifier | q1 state
					self.line_accumulator += char
					self.state = 1
				elif(re.match(r'[0-9]', char)): # this is a number | q2 state
					self.line_accumulator += char
					self.state = 2
				elif(char == "+"):
					self.line_accumulator += char
					self.state = 3
				elif(char == "*"):				
					self.line_accumulator += char
					self.store_token_and_reset(20, line_key)
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
				elif(char == '/'): # this can be a aritmetic operator, a line comment or a block comment | q11 state
					self.line_accumulator += char
					self.state = 11
				elif(char == ';'):
					self.line_accumulator += char
					self.store_token_and_reset(5, line_key)
				elif(char == ','):
					self.line_accumulator += char
					self.store_token_and_reset(6, line_key)
				elif(char == '('):
					self.line_accumulator += char
					self.store_token_and_reset(7, line_key)
				elif(char == ')'):
					self.line_accumulator += char
					self.store_token_and_reset(8, line_key)
				elif(char == '['):
					self.line_accumulator += char
					self.store_token_and_reset(9, line_key)
				elif(char == ']'):
					self.line_accumulator += char
					self.store_token_and_reset(10, line_key)
				elif(char == '{'):
					self.line_accumulator += char
					self.store_token_and_reset(11, line_key)
				elif(char == '}'):
					self.line_accumulator += char
					self.store_token_and_reset(12, line_key)
				elif(char == '.'):
					self.line_accumulator += char
					self.store_token_and_reset(13, line_key)
				else:
					if(char != " " and char != "\t" and char != "\n"):
						self.line_accumulator += char
						self.store_token_and_reset(33, line_key)

			case 1: # process q1 state
				if(re.match(r'[A-Z]|[a-z]', char) or re.match(r'[0-9]', char) or (char == '_')):
					self.line_accumulator += char
				else: # build a identifier token and return to process character function
					self.store_token_and_reset(1, line_key)
					self.process_character(char, line_key)

			case 2:
				if(re.match(r'[0-9]', char)):
					self.line_accumulator += char
				elif(char == '.'):
					self.line_accumulator += char
					self.state = 6
				else: # build a number token and return to process character function
					self.store_token_and_reset(2, line_key)
					self.process_character(char, line_key)

			case 3:
				if(char == "+"): # this store a ++
					self.line_accumulator += char
					self.store_token_and_reset(18, line_key)
				else: #this store a +
					self.store_token_and_reset(17, line_key)
					self.process_character(char, line_key)

			case 4:
				if(char == "-"): # this store a --
					self.line_accumulator += char
					self.store_token_and_reset(22, line_key)
				elif(re.match(r'[0-9]', char)): # checks if is - followed by number
					self.line_accumulator += char
					self.state = 2
				elif(re.match(r'[A-Z]|[a-z]', char)):  # checks if is - followed by letter
					self.store_token_and_reset(21, line_key)
					self.line_accumulator += char
					self.state = 1
				else:
					if(char != " "):# checks if is a space
						self.line_accumulator += char
					self.state = 18
			case 5:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(23, line_key)
				else:
					self.store_token_and_reset(30, line_key)
					self.process_character(char, line_key)

			case 6:
				if(re.match(r'[0-9]', char)):
					self.line_accumulator += char
					self.state = 7
				else:
					self.store_token_and_reset(16, line_key)
					self.process_character(char, line_key)

			case 7:
				if(re.match(r'[0-9]', char)):
					self.line_accumulator += char
				else:
					self.store_token_and_reset(2, line_key)
					self.process_character(char, line_key)

			case 8:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(24, line_key)
				else:
					self.store_token_and_reset(29, line_key)
					self.process_character(char, line_key)

			case 9:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(28, line_key)
				else:
					self.store_token_and_reset(27, line_key)
					self.process_character(char, line_key)

			case 10:
				if(char == "="):
					self.line_accumulator += char
					self.store_token_and_reset(26, line_key)
				else:
					self.store_token_and_reset(25, line_key)
					self.process_character(char, line_key)

			case 11:
				if(char == '/'): # this means that the rest of the line is a comment
					self.line_accumulator += char
					self.state = 12
				elif(char == '*'): # this means that is a block comment
					self.line_accumulator += char
					self.state = 13
				else:
					self.store_token_and_reset(19, line_key)
					self.process_character(char, line_key)

			case 12: # this is a line block
				if(char == "\n"):
					self.store_token_and_reset(3, line_key)
				else:
					self.line_accumulator += char

			case 13: # this is a intermediate state for a block comment 
				self.line_accumulator += char
				if(char == '*'):
					self.state = 14

			case 14: # this is a block comment 
				self.line_accumulator += char
				if(char == '/'):
					self.store_token_and_reset(4, line_key)
				else:
					self.state = 13

			case 15: # this is a string
				self.line_accumulator += char
				if(char == '"'):
					self.store_token_and_reset(0, line_key)
				elif(char == '\n'):
					self.store_token_and_reset(14, line_key)

			case 16:
				if (char == "&"):
					self.line_accumulator += char
					self.store_token_and_reset(31, line_key)
				else:
					self.store_token_and_reset(33, line_key)
					self.process_character(char, line_key)

			case 17:
				if (char == "|"):
					self.line_accumulator += char
					self.store_token_and_reset(32, line_key)
				else:
					self.store_token_and_reset(33, line_key)
					self.process_character(char, line_key)

			case 18: 
				if(self.token_list[-1]['type'] =="NUMBER" or self.token_list[-1]['type'] =="IDENTIFIER"):# checks if the last token was a number or identifier
					self.store_token_and_reset(21, line_key)
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
					self.store_token_and_reset(21, line_key)
					self.process_character(char, line_key)

	def show_token_list(self):
		return self.token_list;

	def store_token_and_reset(self, token_type, line):
		self.token_list.append(token.Token.generate_token(token_type, self.line_accumulator, line+1))
		self.state = 0
		self.line_accumulator = ''