class Processor:
	def __init__(self):
		self.token_in_line = 0
		self.line = 0

	def process_tokens(self, tokens):
		for token in tokens:
			print(token)