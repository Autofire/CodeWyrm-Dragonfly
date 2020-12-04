from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, Text
from base import fluid

print("Loading grammar: java")

"""
special_rule = MappingRule(
	name = "rust special",
	mapping = {
		"print line": Function(wrapped_insert, start="System.out.println(", end = ");"),
		},
	extras = [

		],
)
"""


kw_rules = {}

keywords = [
"False", "await", "else", "import", "pass",
"None", "break", "except", "in", "raise",
"True", "class", "finally", "is", "return",
"and", "continue", "for", "lambda", "try",
"as", "def", "from", "nonlocal", "while",
"assert", "del", "global", "not", "with",
"elif", "if", "or", "yield",
]
for keyword in keywords:
	kw_rules[keyword] = Text(keyword)
kw_rules["a sink"] = Text("async")
kw_rules["else if"] = Text("elif")
kw_rules["define"] = Text("def")

keyword_rule = MappingRule( name = "python keywords", mapping = kw_rules )


def build_grammar(context):
	grammar = Grammar("python", context=(context))
	#grammar.add_rule(keyword_rule)  
	#grammar.add_rule(special_rule)
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))  
	return grammar
