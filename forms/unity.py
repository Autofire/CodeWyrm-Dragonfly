from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert 

print("Loading grammar: unity")

language_rule = MappingRule(
	name = "unity",
	mapping = {
		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("unity", context=(context))
	grammar.add_rule(language_rule)  
	return grammar
