from dragonfly import (Grammar, CompoundRule, AppContext)

#from forms import *

import forms.vim
import forms.bash

grammars = []

def load_forms():
	reload(forms.vim)
	reload(forms.bash)
	config_forms()

def config_forms():
	global grammars
	#grammars = []

	putty_context = AppContext(title="bash")
	extraterm_context = AppContext(executable="extraterm")

	bash_context = putty_context | extraterm_context;

	vim_context = extraterm_context

	#bash_grammar = forms.bash.build_grammar(bash_context)
	#bash_grammar.load()
	#forms.bash.grammar.context = bash_context
	#forms.bash.grammar.load()

	grammars = [
		forms.bash.build_grammar(bash_context),
		forms.vim.build_grammar(vim_context)
	]

	for grammar in grammars:
		grammar.load()

def unload_forms():
	global grammars
	for grammar in grammars:
		grammar.unload()
	grammars = []

class FormReloader(CompoundRule):
	spec = "dragon refresh"


	def _process_recognition(self, node, extras): 
		print("Reloading...")
		unload_forms()
		load_forms()
		print("Done.")
		print("")


formGrammar = Grammar("form handler")                
formGrammar.add_rule(FormReloader())
formGrammar.load()

print("Doing first config...")
config_forms()
print("Done.")
print("")

# Unload function which will be called by natlink at unload time.
def unload():
	global formGrammar
	if formGrammar: formGrammar.unload()
	formGrammar = None
	unload_forms()


