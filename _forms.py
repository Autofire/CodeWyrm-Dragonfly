from dragonfly import (Grammar, CompoundRule)

#from forms import *

import forms.vim
import forms.bash


class FormReloader(CompoundRule):
	spec = "dragon refresh"

	def _process_recognition(self, node, extras): 
		print("Reloading...")
		unload_forms()
		reload(forms.vim)
		reload(forms.bash)
		#forms.bash.grammar.load()
		print("Done.")
		print("")


formGrammar = Grammar("form handler")                
formGrammar.add_rule(FormReloader())
formGrammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
	global formGrammar
	if formGrammar: formGrammar.unload()
	formGrammar = None
	unload_forms()

def unload_forms():
	forms.vim.unload()
	forms.bash.unload()

