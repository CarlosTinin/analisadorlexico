import token
import re

class Processor:
	def __init__(self):
		self.token_list = []
		self.ids = 0
		self.state = 0
		self.line_accumulator = ''

	def process_file(self, file):
		for line in file.readlines():
			for char in line:
				self.process_character(char)
		else:
			if (self.state ==  13):
				self.store_token_and_reset(self.ids, 15, self.line_accumulator)

	def process_character(self, char):
		if (self.state == 0):
			if(re.match(r'[A-Z]|[a-z]', char)): # this is a identifier | q1 state
				self.line_accumulator += char
				self.state = 1
			elif(char == '"'):
				self.line_accumulator += char
				self.state = 15
			elif(char == '/'): # this can be a aritmetic operator, a line comment or a block comment | q11 state
				self.line_accumulator += char
				self.state = 11
			elif(char == ';'):
				self.store_token_and_reset(self.ids, 5, self.line_accumulator)
			elif(char == ','):
				self.store_token_and_reset(self.ids, 6, self.line_accumulator)
			elif(char == '('):
				self.store_token_and_reset(self.ids, 7, self.line_accumulator)
			elif(char == ')'):
				self.store_token_and_reset(self.ids, 8, self.line_accumulator)
			elif(char == '['):
				self.store_token_and_reset(self.ids, 9, self.line_accumulator)
			elif(char == ']'):
				self.store_token_and_reset(self.ids, 10, self.line_accumulator)
			elif(char == '{'):
				self.store_token_and_reset(self.ids, 11, self.line_accumulator)
			elif(char == '}'):
				self.store_token_and_reset(self.ids, 12, self.line_accumulator)
			elif(char == '.'):
				self.store_token_and_reset(self.ids, 13, self.line_accumulator)
		elif (self.state == 1): # process q1 state
			if(re.match(r'[A-Z]|[a-z]', char) or re.match(r'[1-9]', char) or (char == '_')):
				self.line_accumulator += char
			else: # build a identifier token and return to process character function
				self.store_token_and_reset(self.ids, 1, self.line_accumulator)
				self.process_character(char)

		elif (self.state == 11):
			if(char == '/'): # this means that the rest of the line is a comment
				self.line_accumulator += char
				self.state = 12
			elif(char == '*'): # this means that is a block comment
				self.line_accumulator += char
				self.state = 13

		elif (self.state == 12): # this is a line block
			if(char == "\n"):
				self.store_token_and_reset(self.ids, 3, self.line_accumulator)
			else:
				self.line_accumulator += char

		elif(self.state == 13): # this is a intermediate state for a block comment 
			self.line_accumulator += char
			if(char == '*'):
				self.state = 14

		elif(self.state == 14): # this is a block comment 
			self.line_accumulator += char
			if(char == '/'):
				self.store_token_and_reset(self.ids, 4, self.line_accumulator)
			else:
				self.state = 13

		elif (self.state == 15): # this is a string
			self.line_accumulator += char
			if(char == '"'):
				self.store_token_and_reset(self.ids, 0, self.line_accumulator)
			elif(char == '\n'):
				self.store_token_and_reset(self.ids, 14, self.line_accumulator)

	def show_token_list(self):
		return self.token_list;

	def store_token_and_reset(self, token_id, token_type, content):
		self.token_list.append(token.Token.generate_token(token_id, token_type, content))
		self.ids += 1
		self.state = 0
		self.line_accumulator = ''