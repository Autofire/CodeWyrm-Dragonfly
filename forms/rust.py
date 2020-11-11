from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert, do_insert

print("Loading grammar: rust")

special_rule = MappingRule(
	name = "rust special",
	mapping = {
		"print line": Function(wrapped_insert, start="println!(", end = ");"),
		"small arrow": Function(insert, action=Text("->")),
		"big arrow": Function(insert, action=Text("=>")),
		"in out": Function(insert, action=Text("io")),

		"standard in": Function(insert, action=Text("stdin")),
		"standard out": Function(insert, action=Text("stdout")),
		"standard": Function(insert, action=Text("std")),

		"okay": Function(insert, action=Text("Ok")),
		"error": Function(insert, action=Text("Err")),

		"compare": Function(insert, action=Text("cmp")),

		"say numb": Function(insert, action=Text("num")),
		"say guess": Function(insert, action=Text("guess")),

		},
	extras = [

		],
)


kw_rules = {}

simple_keywords = [
"as",
"use",
"extern crate",
"break",
"const",
"continue",
"crate",
"else",
"if",
"enum",
"extern",
"false",
"for",
"if",
"impl",
"in",
"for",
"let",
"loop",
"match",
"mod",
"move",
"mut",
"pub",
"impl",
"ref",
"return",
"Self",
"self",
"static",
"struct",
"super",
"trait",
"true",
"type",
"unsafe",
"use",
"where",
"while",
"abstract",
"become",
"box",
"do",
"final",
"macro",
"override",
"priv",
"proc",
"pure",
"unsized",
"virtual",
"yield",
]
for keyword in simple_keywords:
	kw_rules[keyword] = do_insert(keyword)

complex_kw = {
	"size of": "sizeof",
	"type of": "typeof",
	"align of": "alignof",
	"offset of": "offsetof",
	"function": "fn",
	"vector": "Vec",
	"length": "len",
}
for key in complex_kw:
	kw_rules[key] = do_insert(complex_kw[key])

signed_prefix = "int "
unsigned_prefix = "you "
types = [ "8", "16", "32", "64", "128", "size" ]
for t in types:
	kw_rules[signed_prefix + t] = do_insert("i"+t)
	kw_rules[unsigned_prefix + t] = do_insert("u"+t)

kw_rules["float 32"] = do_insert("f32")
kw_rules["float 64"] = do_insert("f64")
kw_rules["bool"] = do_insert("bool")
kw_rules["care"] = do_insert("char")

keyword_rule = MappingRule( name = "rust keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("rust", context=(context))
	grammar.add_rule(keyword_rule)  
	grammar.add_rule(special_rule)  
	return grammar
