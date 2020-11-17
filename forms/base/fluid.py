from dragonfly import (Grammar, AppContext,
                       MappingRule, CompoundRule,
                       Dictation, Integer, Repeat,
					   IntegerRef, RuleRef, Impossible,
					   Literal, Sequence, Repetition, Alternative,
                       Key, Text, Function, ActionBase)
from vim import (start_insert, end_insert)

# Credit for most of this logic goes to Christo Butcher and David Gessner
# TODO Get URL
class SymbolRule(MappingRule):
    name = "symbol"
    exported = False
    mapping = {
		"colon":       Key("colon"),
		"semi[colon]": Key("semicolon"),
    	"(com|comma)": Key('comma'),
    	"equals":      Key('='),
    	"bang":        Key('!'),
    	"dot":         Key('.'),
    	"amp":         Key('&'),
    	"quest":       Key('?'),
		"hash":        Key("#"),
		"pipe":        Key("|"),
		"squiggle":    Key("~"),

		"(minus|dash)":   Key("minus"),
		"plus":           Key("plus"),
		"(slash|divide)": Key("slash"),
		"(star|times)":   Key("star"),
		"(mod|percent)":  Key("percent"),

		"space":     Key("space"),
		"backslash": Key("backslash"),
		"tab":       Key("tab"),
		"score":     Key("underscore"),

		"len":       Key("("),
		"ren":       Key(")"),
		"lace":      Key("{"),
		"race":      Key("}"),
		"lack":      Key("["),
		"rack":      Key("]"),
        "langle":    Key('langle'),
        "rangle":    Key('rangle'),

        "single":    Key('squote'),
        "double":    Key('dquote'),

		"slap":      Key('enter'),
	}

letter_names = [
	'apple', 'beetle', 'club', 'diamond', 'egg', 'flame',
	'giga', 'heart', 'index', 'jack', 'king', 'limbo',
	'mule', 'net', 'oak', 'page', 'queen', 'raft',
	'spade', 'tide', 'use', 'vast', 'whale', 'x-ray',
	'yacht', 'zed'
]
print(letter_names)

letter_map = {
	'zero':  Key('0'),
	'one':   Key('1'),
	'two':   Key('2'),
	'three': Key('3'),
	'four':  Key('4'),
	'five':  Key('5'),
	'six':   Key('6'),
	'seven': Key('7'),
	'eight': Key('8'),
	'nine':  Key('9'),
}
for name in letter_names:
	letter_map[name] = Key(name[0], static=True)
	letter_map["cap " + name] = Key(name[0].upper(), static=True)

class LetterRule(MappingRule):
    name = "letter"
    exported = False
    mapping = letter_map 


def execute_symbol(symbol):
	symbol.execute()

def execute_symbol_sequence(symbol_sequence):
	for symbol in symbol_sequence:
		symbol.execute()


def build_rule(custom_symbol=Impossible()):

	symbol = Alternative([RuleRef(rule=SymbolRule()), custom_symbol], name='symbol')
	letter = RuleRef(rule=LetterRule(), name='letter')

	symbol_sequence = Repetition(
		Alternative([letter, symbol]),
		min=1, max=32, name='symbol_sequence'
	)

	spell_rule = MappingRule(
		name = "letter mapping",
		mapping = {
			"press <symbol_sequence>": Function(execute_symbol_sequence),
			"spell <symbol_sequence>":
				Function(start_insert)
				  + Function(execute_symbol_sequence)
				  + Function(end_insert),

			# TODO Figure out how to bundle this into the rule below via defaults
			"<symbol>":
				Function(start_insert)
				  #+ Function(execute_symbol)
				  + Function(lambda symbol: symbol.execute())
				  + Function(end_insert),

			"<symbol> <symbol_sequence>":
				Function(start_insert)
				  + Function(execute_symbol)
				  + Function(execute_symbol_sequence)
				  + Function(end_insert),
		},
		extras = [
			symbol_sequence,
			symbol,
		],
	)

	return spell_rule

	
