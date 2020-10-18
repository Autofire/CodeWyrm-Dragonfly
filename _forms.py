from dragonfly import (Grammar, CompoundRule, AppContext, FuncContext,
                       MappingRule, Function, PlaySound)

#from forms import *

import forms.vim
import forms.bash
import forms.rust

# TODO Maybe remove this?
import logging
logging.basicConfig()

"""
========================================================================
= Sounds
========================================================================
"""
sound_path = "C:\\Users\\Daniel\\DragonSounds\\mmbn\\"
sounds = {
	"refresh": sound_path + "refresh.wav",
	"error": sound_path + "error.wav",
	"shift": sound_path + "shift.wav",
	"revert": sound_path + "revert.wav",
}
def play_sound(name):
	PlaySound(file=sounds[name]).execute()


"""
========================================================================
= Form config
========================================================================
"""
grammars = []

_bash_vim = False
def bash_vim(value=None):
	global _bash_vim

	if value is not None:
		if value != _bash_vim:
			if value:
				play_sound("shift")
			else:
				play_sound("revert")
		_bash_vim = value
		print("Overriding Bash with VIM: ", value)

	return _bash_vim

def load_forms():
	reload(forms.vim)
	reload(forms.bash)
	reload(forms.rust)
	config_forms()

def config_forms():
	global grammars
	#grammars = []

	putty_context = AppContext(title="bash")
	extraterm_context = AppContext(executable="extraterm")

	bash_base_context = putty_context | extraterm_context;
	vim_bash_override_context = FuncContext(bash_vim) | AppContext(title="VIM")

	bash_context = (bash_base_context & ~vim_bash_override_context)
	vim_context  = (bash_base_context & vim_bash_override_context)

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


"""
========================================================================
= Form control
========================================================================
"""
class FormReloader(CompoundRule):
	spec = "dragon refresh"

	def _process_recognition(self, node, extras): 
		print("Reloading...")
		try:
			unload_forms()
			load_forms()
			print("Done.")
			print("")
			play_sound("refresh")
		except:
			play_sound("error")
			raise
		#except Exception as e:
			#raise e

shift_rule = MappingRule(
	name = "shift",
	mapping = {
		"dragon shift vim":  Function(bash_vim, value=True),
		"dragon revert vim": Function(bash_vim, value=False),
	},
	extras = [
	],
)

formGrammar = Grammar("form handler")                
formGrammar.add_rule(FormReloader())
formGrammar.add_rule(shift_rule)
formGrammar.load()



print("Doing first config...")
config_forms()
print("Done.")
print("")
play_sound("refresh")

# Unload function which will be called by natlink at unload time.
def unload():
	global formGrammar
	if formGrammar: formGrammar.unload()
	formGrammar = None
	unload_forms()


