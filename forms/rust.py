from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
import vim

print("Loading grammar: rust")






def build_grammar(context):
	grammar = Grammar("rust", context(context))
	grammar.add_rule(rust_rule)  
	return grammar
