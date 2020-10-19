from sys import stdout
from dragonfly import (Grammar, CompoundRule, AppContext, FuncContext,
                       MappingRule, Function, PlaySound)

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
= Initial import
========================================================================
"""
try:
	import forms.vim
	import forms.bash
	import forms.rust
except:
	play_sound("error")
	raise


"""
========================================================================
= Form config
========================================================================
"""
form_grammars = []

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

def load_forms(unload=False):
	global form_grammars

	try:
		if unload:
			print("Reloading forms...")
			reload(forms.vim)
			reload(forms.bash)
			reload(forms.rust)
		else:
			print("Performing first config...")
			
		# Do this before unloading in case of exception
		new_form_grammars = build_form_grammars()

		# Always safe to unload
		unload_forms()

		form_grammars = new_form_grammars

		for grammar in form_grammars:
			grammar.load()
		print("Done.\n")
		play_sound("refresh")
	except:
		play_sound("error")
		raise
		

def build_form_grammars():
	#global form_grammars
	#form_grammars = []

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

	new_form_grammars = [
		forms.bash.build_grammar(bash_context),
		forms.vim.build_grammar(vim_context),
		forms.rust.build_grammar(vim_context),
	]

	return new_form_grammars


def unload_forms():
	stdout.write("Unloading forms...")
	global form_grammars
	for grammar in form_grammars:
		grammar.unload()
	
	if len(form_grammars) > 0:
		print("done.")
	else:
		print("nothing to unload.")

	form_grammars = []


"""
========================================================================
= Form control
========================================================================
"""
class FormReloader(CompoundRule):
	spec = "dragon refresh"

	def _process_recognition(self, node, extras): 
		load_forms(unload=True)

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


load_forms()

# Unload function which will be called by natlink at unload time.
def unload():
	global formGrammar
	if formGrammar: formGrammar.unload()
	formGrammar = None
	unload_forms()



