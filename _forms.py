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
	import forms.cpp
	import forms.cs
	import forms.java
	import forms.python

	import forms.unity
	import forms.unreal

except:
	play_sound("error")
	raise


"""
========================================================================
= Form config
========================================================================
"""
grammars = []

# Generate our form tags
# We could use strings but that's gross
L_NONE, L_CPP, L_CS, L_JAVA, L_PYTHON, L_RUST, L_UNITY, L_UNREAL = range(8)

# First is print, second is spoken. If just one, they are same.
form_names = {
	L_NONE: ["None", "!None"],
	L_CPP: ["C++", "C plus plus"],
	L_CS: ["C#", "C sharp"],
	L_JAVA: ["Java"],
	L_PYTHON: ["Python"],
	L_RUST: ["Rust"],
	L_UNITY: ["Unity"],
	L_UNREAL: ["Unreal"],
}
_active_form = L_NONE

def form_written(form):
	return form_names[form][0]

def form_spoken(form):
	names = form_names[form]
	if len(names) > 1:
		return names[1]
	else:
		return names[0]
	
def build_form_context(form):
	def is_in_form():
		return active_form() == form

	return FuncContext(is_in_form) 


def active_form(value=None):
	global _active_form

	if value is not None:
		if value == _active_form:
			print("Already in " + form_written(_active_form))
		elif value == L_NONE:
			print("Reverting " + form_written(_active_form))
			_active_form = L_NONE
			play_sound("revert")
		else:
			print("Switching from " + form_written(_active_form) + " to " + form_written(value))
			_active_form = value
			play_sound("shift")
				
	return _active_form

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
	global grammars

	try:
		if unload:
			print("Reloading forms...")
			reload(forms.bash)
			reload(forms.vim)

			reload(forms.rust  )
			reload(forms.cpp   )
			reload(forms.cs    )
			reload(forms.java  )
			reload(forms.python)
			reload(forms.unity)
			reload(forms.unreal)
		else:
			print("Performing first config...")
			
		# Do this before unloading in case of exception
		new_grammars = build_grammars()

		# Always safe to unload
		unload_forms()

		grammars = new_grammars

		for grammar in grammars:
			grammar.load()
		print("Done.\n")
		play_sound("refresh")
	except:
		play_sound("error")
		raise
		

def build_grammars():
	putty_context = AppContext(title="bash")
	extraterm_context = AppContext(executable="extraterm")
	netbeans_context = AppContext(executable="netbeans64")
	intellij_context = AppContext(executable="idea64")
	vs_context = AppContext(title="Visual Studio")

	bash_base_context = putty_context | extraterm_context;
	vim_bash_override_context = FuncContext(bash_vim) | AppContext(title="VIM")

	bash_context = (bash_base_context & ~vim_bash_override_context)
	
	bash_vim_context = (bash_base_context & vim_bash_override_context)
	vim_context = bash_vim_context | netbeans_context | intellij_context | vs_context

	java_context = vim_context & (build_form_context(L_JAVA) | netbeans_context | intellij_context)

	new_grammars = [
		forms.bash.build_grammar(bash_context),
		forms.vim.build_grammar(vim_context),

		forms.rust  .build_grammar(vim_context & build_form_context(L_RUST)),
		forms.cpp   .build_grammar(vim_context & build_form_context(L_CPP)),
		forms.cs    .build_grammar(vim_context & build_form_context(L_CS)),
		#forms.java  .build_grammar(vim_context & build_form_context(L_JAVA)),
		forms.java  .build_grammar(java_context),
		#forms.python.build_grammar(vim_context & build_form_context(L_PYTHON)),

		#forms.unity .build_grammar(vim_context & build_form_context(L_UNITY)),
		#forms.unreal.build_grammar(vim_context & build_form_context(L_UNREAL)),
	]
	#new_grammars = {
	#	'_bash': forms.bash.build_grammar(bash_context),
	#	'_vim':  forms.vim.build_grammar(vim_context),
	#
	#	'rust': forms.rust.build_grammar(vim_context),
	#}

	return new_grammars


def unload_forms():
	global grammars

	if len(grammars) > 0:
		stdout.write("Unloading forms...")

	for grammar in grammars:
		grammar.unload()
	
	if len(grammars) > 0:
		print("done.")

	grammars = []


"""
========================================================================
= Form control
========================================================================
"""
control_rule = MappingRule(
	name = "control",
	mapping = {
		"dragon enable vim":  Function(bash_vim, value=True),
		"dragon disable vim": Function(bash_vim, value=False),
		"dragon refresh":     Function(load_forms, unload=True),
	},
	extras = [
	],
)

form_rule_mapping = {}
for form in form_names.keys(): 
	form_rule_mapping["dragon shift " + form_spoken(form)] = Function(active_form, value=form)

form_rule_mapping["dragon revert"] = Function(active_form, value=L_NONE)

form_rule = MappingRule(
	name = "forms",
	mapping = form_rule_mapping,
)

control_grammar = Grammar("form handler")                
control_grammar.add_rule(control_rule)
control_grammar.add_rule(form_rule)
control_grammar.load()

load_forms(unload=True)

# Unload function which will be called by natlink at unload time.
def unload():
	global control_grammar
	if control_grammar: control_grammar.unload()
	control_grammar = None
	unload_forms()



