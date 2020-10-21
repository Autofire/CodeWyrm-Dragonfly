from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert 

print("Loading grammar: rust")

rust_rule = MappingRule(
	name = "rust",
	mapping = {
		"print line": Function(wrapped_insert, start="println!(", end = ");"),
		"arrow": Function(insert, action=Text("=>")),
		"function": Function(insert, action=Text("fn")),
		"mut": Function(insert, action=Text("mut")),
		"let": Function(insert, action=Text("let")),
		"in out": Function(insert, action=Text("io")),

		"standard in": Function(insert, action=Text("stdin")),
		"standard out": Function(insert, action=Text("stdout")),
		"standard": Function(insert, action=Text("std")),

		"okay": Function(insert, action=Text("Ok")),
		"error": Function(insert, action=Text("Err")),

		"compare": Function(insert, action=Text("cmp")),

		"say numb": Function(insert, action=Text("num")),
		"say guess": Function(insert, action=Text("guess")),

		"unsigned thirty two": Function(insert, action=Text("u32")),

		},
	extras = [

		],
)


def build_grammar(context):
	grammar = Grammar("rust", context=(context))
	grammar.add_rule(rust_rule)  
	return grammar
