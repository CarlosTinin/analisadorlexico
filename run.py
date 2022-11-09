from lexico.analisadorlexico import *
from sintatico.analisadorsintatico import *

for file, lexical in analiseLexica().items():
  analiseSintatica(file, lexical)