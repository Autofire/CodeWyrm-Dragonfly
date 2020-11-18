from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base import fluid

print("Loading grammar: python")

kw_rules = {}

keywords = [
"while"
]
for keyword in keywords:
	kw_rules[keyword] = Text(keyword)

keyword_rule = MappingRule( name = "python keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("python", context=(context))
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))  
	return grammar
