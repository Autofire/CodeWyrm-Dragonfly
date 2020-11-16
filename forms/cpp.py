from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, do_insert

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
	kw_rules[keyword] = do_insert(keyword)

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
	kw_rules[word] = do_insert(complex_words[word])

variable_prefix = "var "
variables = {
}
for word in variables:
	kw_rules[variable_prefix + word] = do_insert(variables[word])

types = [
	"byte", "short", "int", "long",
	"float", "double",
	"bool", "char",
	"void"
]
for t in types:
	kw_rules["data " + t] = do_insert(t)
kw_rules["data integer"] = do_insert("int")
kw_rules["data (character|care)"] = do_insert("char")


keyword_rule = MappingRule( name = "C++ keywords", mapping = kw_rules )


def build_grammar(context):
	grammar = Grammar("cpp", context=(context))
	grammar.add_rule(keyword_rule)  
	return grammar
