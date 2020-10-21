from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert 

print("Loading grammar: java")

language_rule = MappingRule(
	name = "java",
	mapping = {
		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("java", context=(context))
	grammar.add_rule(language_rule)  
	return grammar
