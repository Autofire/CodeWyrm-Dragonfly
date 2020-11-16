from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, do_insert

print("Loading grammar: java")

kw_rules = {}

keywords = [
	"import", "package",
	"class", "enum", "interface",
	"const", "final", "static",
	"private", "protected", "public",
	"for", "while", "if", "else", "switch",
	"this", "this", "new", "return",
	"throw", "throws", "volatile", "catch", "finally",
]
for keyword in keywords:
	kw_rules[keyword] = do_insert(keyword)
kw_rules["instance of"] = do_insert("instanceof")
kw_rules["GL"] = do_insert("gl")

types = [
	"byte", "short", "int", "long",
	"float", "double",
	"boolean", "char",
	"void"
]
for t in types:
	kw_rules["data " + t] = do_insert(t)
kw_rules["data integer"] = do_insert("int")
kw_rules["data (character|care)"] = do_insert("char")

boxed_types = [
	"Byte", "Short", "Integer", "Long",
	"Float", "Double",
	"Boolean", "Character"
]
for t in boxed_types:
	kw_rules["boxed " + t] = do_insert(t)
kw_rules["boxed care"] = do_insert("Character")
kw_rules["boxed int"] = do_insert("Integer")


keyword_rule = MappingRule( name = "java keywords", mapping = kw_rules )


def build_grammar(context):
	grammar = Grammar("java", context=(context))
	grammar.add_rule(keyword_rule)  
	return grammar
