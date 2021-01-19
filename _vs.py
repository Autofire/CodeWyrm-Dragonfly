from sys import stdout
from dragonfly import (Grammar, CompoundRule, AppContext, FuncContext,
                       MappingRule, Key)

vs_context = AppContext(executable="devenv")
vs_rule = MappingRule(
	name = "vs",
	mapping = {
		"line comment": Key("c-k") + Key("c-c"),
		"line uncomment": Key("c-k") + Key("c-u"),
	},
	extras = [
	],
)

vs_grammar = Grammar("vs grammar", context=vs_context)
vs_grammar.add_rule(vs_rule)
vs_grammar.load()
