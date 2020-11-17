from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, do_insert
from base import fluid

print("Loading grammar: cpp")

kw_rules = {}

keywords = [
"auto",
"break",
"case",
"catch",
"class",
"const",
"continue",
"delete",
"do",
"else",
"enum",
"explicit",
"false",
"for",
"friend",
"goto",
"if",
"inline",
"namespace",
"new",
"noexcept",
"operator",
"private",
"protected",
"public",
"return",
"signed",
"sizeof",
"static",
"struct",
"switch",
"template",
"this",
"throw",
"true",
"try",
"typedef",
"typeid",
"typename",
"union",
"unsigned",
"virtual",
"while",
]
for keyword in keywords:
	kw_rules[keyword] = Text(keyword)

complex_words = {
"static assert": "static_assert",
"static cast": "static cast",
"null pointer": "nullptr",
"dynamic cast": "dynamic_cast",
"const eval": "consteval",
"const expression": "constexpr",
"const cast": "const_cast",

"arg count": "argc",
"arg vector": "argv",
"C out": "cout",
"C in": "cin",
"C err": "cerr",
"end L": "endl",
}
for word in complex_words:
	kw_rules[word] = Text(complex_words[word])

variable_prefix = "var "
variables = {
}
for word in variables:
	kw_rules[variable_prefix + word] = Text(variables[word])

types = [
	"byte", "short", "int", "long",
	"float", "double",
	"bool", "char",
	"void"
]
for t in types:
	kw_rules["data " + t] = Text(t)
kw_rules["data integer"] = Text("int")
kw_rules["data (character|care)"] = Text("char")


keyword_rule = MappingRule( name = "C++ keywords", mapping = kw_rules )


def build_grammar(context):
	grammar = Grammar("cpp", context=(context))
	#grammar.add_rule(keyword_rule)  
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))  
	return grammar
