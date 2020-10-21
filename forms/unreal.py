from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert 

print("Loading grammar: unreal")

language_rule = MappingRule(
	name = "unreal",
	mapping = {
		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("unreal", context=(context))
	grammar.add_rule(language_rule)  
	return grammar
