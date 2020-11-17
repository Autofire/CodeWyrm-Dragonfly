from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert 
from base import fluid

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
	#grammar.add_rule(language_rule)  
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))
	return grammar
