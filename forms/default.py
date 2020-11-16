from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, do_insert

print("Loading grammar: default")

kw_rules = {}

keywords = [
"while"
]
for keyword in keywords:
	kw_rules[keyword] = do_insert(keyword)

keyword_rule = MappingRule( name = "default keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("default", context=(context))
	grammar.add_rule(keyword_rule)  
	return grammar
