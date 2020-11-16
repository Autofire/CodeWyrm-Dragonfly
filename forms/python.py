from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert 

print("Loading grammar: python")

language_rule = MappingRule(
	name = "python",
	mapping = {
		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("python", context=(context))
	grammar.add_rule(language_rule)  
	return grammar
