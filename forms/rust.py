from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert
from base import fluid

print("Loading grammar: rust")

special_rule = MappingRule(
	name = "rust special",
	mapping = {
		"print line": Function(wrapped_insert, start="println!(", end = ");"),
		},
	extras = [

		],
)

kw_rules = {}

simple_keywords = [
"as", "use",
"break", "const", "continue",
"crate", "else", "if",
"enum", "extern", "false",
"for", "if", "impl",
"in", "for", "let",
"loop", "match",
"move", "mut", "pub",
"impl", "ref", "return",
"self", "static",
"struct", "super", "trait",
"true", "type", "unsafe",
"use", "where", "while",
"abstract", "become", "box",
"do", "final", "macro",
"override", "priv", "proc",
"pure", "unsized", "virtual",
"yield",

"self",
"io",
]
for keyword in simple_keywords:
	kw_rules[keyword] = Text(keyword)

complex_kw = {
	"size of": "sizeof",
	"type of": "typeof",
	"align of": "alignof",
	"offset of": "offsetof",
	"function": "fn",
	"length": "len",
	"cap self": "Self",
	"module": "mod",

	"vector": "Vec",


	"standard in": "stdin",
	"standard out": "stdout",
	"standard": "std",

	"okay": "Ok",
	"error": "Err",

	"compare": "cmp",
        "context": "ctx",
}
for key in complex_kw:
	kw_rules[key] = Text(complex_kw[key])

signed_prefix = "int "
unsigned_prefix = "you "
types = [ "8", "16", "32", "64", "128", "size" ]
for t in types:
	kw_rules[signed_prefix + t] = Text("i"+t)
	kw_rules[unsigned_prefix + t] = Text("u"+t)

kw_rules["float 32"] = Text("f32")
kw_rules["float 64"] = Text("f64")
kw_rules["bool"] = Text("bool")
kw_rules["care"] = Text("char")

keyword_rule = MappingRule( name = "rust keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("rust", context=(context))
	#grammar.add_rule(keyword_rule)  
	grammar.add_rule(special_rule)  
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))
	return grammar
