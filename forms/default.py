from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, do_insert
from base.fluid import build_rule

print("Loading grammar: default")

kw_rules = {}

keywords = [
"while"
]
for keyword in keywords:
	kw_rules[keyword] = Text(keyword)

keyword_rule = MappingRule( name = "default keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("default", context=(context))
	#grammar.add_rule(keyword_rule)  
	custom = RuleRef(rule=keyword_rule, name='custom')
	grammar.add_rule(build_rule())
	return grammar
