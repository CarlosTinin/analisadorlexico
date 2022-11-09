from sintatico.processor import Processor

def analiseSintatica(file, tokens):
	proc = Processor() 
	proc.process_tokens(tokens)