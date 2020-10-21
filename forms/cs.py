from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert 

print("Loading grammar: cs")

language_rule = MappingRule(
	name = "cs",
	mapping = {
		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("cs", context=(context))
	grammar.add_rule(language_rule)  
	return grammar
