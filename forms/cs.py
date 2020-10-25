from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert, do_insert

print("Loading grammar: cs")

kw_rules = {}

keywords = [
"abstract", "as", "base",
"break", "case", "catch",
"checked", "class", "const",
"continue", "decimal", "default", "delegate",
"do", "else", "enum",
"event", "explicit", "extern", "false",
"finally", "fixed", "float", "for",
"goto", "if", "implicit",
"in", "interface", "internal",
"is", "lock", "namespace",
"new", "null", "object", "operator",
"out", "override", "params", "private",
"protected", "public", "readonly", "ref",
"return", "sealed", 
"sizeof", "static",
"struct", "switch", "this", "throw",
"true", "try", "typeof",
"unchecked", "unsafe",
"using", "virtual", "volatile",
"while",
]
for keyword in keywords:
	kw_rules[keyword] = do_insert(keyword)
kw_rules["for each"] = do_insert("foreach")
kw_rules["stack alloc"] = do_insert("stackalloc")

type_prefix = "data "
types = [
	"short", "int", "long",
	"float", "double",
	"bool", "char", "string",
	"void"
]
for t in types:
	kw_rules[type_prefix + t] = do_insert(t)
kw_rules[type_prefix + "byte"] = do_insert("sbyte")
kw_rules[type_prefix + "integer"] = do_insert("int")
kw_rules[type_prefix + "(character|care)"] = do_insert("char")

utype_prefix = "data you "
utypes = [
	"short", "int", "long"
]
for t in utypes:
	kw_rules[utype_prefix + t] = do_insert("u" + t)
kw_rules[utype_prefix + "byte"] = do_insert("byte")
kw_rules[utype_prefix + "integer"] = do_insert("uint")

keyword_rule = MappingRule( name = "java keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("cs", context=(context))
	grammar.add_rule(keyword_rule)  
	return grammar
