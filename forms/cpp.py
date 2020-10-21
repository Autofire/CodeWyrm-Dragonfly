from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert, do_insert

print("Loading grammar: cpp")

language_rule = MappingRule(
	name = "cpp",
	mapping = {
		"class": do_insert("class"),
		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("cpp", context=(context))
	grammar.add_rule(language_rule)  
	return grammar
