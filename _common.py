from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef,
                       Key, Text)

grammar = Grammar("common")

general_rule = MappingRule(
	name = "general",
	mapping = {
		"kay": Key("enter"),
		"slap": Key("enter"),
		"left": Key("left"),
		"right": Key("right"),

		"star": Key("*"),
		"dash": Key("-"),
		"minus": Key("-"),
		"space": Key("space"),
		"tab": Key("tab"),
		"score": Key("_"),

		"len": Key("("),
		"ren": Key(")"),
		"lace": Key("{"),
		"race": Key("}"),
		"lack": Key("["),
		"rack": Key("]"),
        'langle': Key('langle'),
        'rangle': Key('rangle'),

		#"say <text>": Text("%(text)s"),
		},
	extras = [
		Dictation("text"),
		],
)

common_name_rule = MappingRule(
	name = "common names",
	mapping = {
		"T. M. P.": Text("tmp"),
		},
	extras = [
		],
)

grammar.add_rule(general_rule)
grammar.add_rule(common_name_rule)
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
