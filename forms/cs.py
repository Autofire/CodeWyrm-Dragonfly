from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, Text
from base import fluid

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
	kw_rules[keyword] = Text(keyword)
kw_rules["for each"] = Text("foreach")
kw_rules["stack alloc"] = Text("stackalloc")

type_prefix = "data "
types = [
	"short", "int", "long",
	"float", "double",
	"bool", "char", "string",
	"void"
]
for t in types:
	kw_rules[type_prefix + t] = Text(t)
kw_rules[type_prefix + "byte"] = Text("sbyte")
kw_rules[type_prefix + "integer"] = Text("int")
kw_rules[type_prefix + "(character|care)"] = Text("char")

utype_prefix = "data you "
utypes = [
	"short", "int", "long"
]
for t in utypes:
	kw_rules[utype_prefix + t] = Text("u" + t)
kw_rules[utype_prefix + "byte"] = Text("byte")
kw_rules[utype_prefix + "integer"] = Text("uint")

keyword_rule = MappingRule( name = "java keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("cs", context=(context))
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))
	return grammar
