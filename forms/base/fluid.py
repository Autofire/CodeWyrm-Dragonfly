from dragonfly import (Grammar, AppContext,
                       MappingRule, CompoundRule,
                       Dictation, Integer, Repeat,
					   IntegerRef, RuleRef, Impossible,
					   Literal, Sequence, Repetition, Alternative,
					   Sequence, Optional,
                       Key, Text, Function, ActionBase)
from vim import (start_insert, end_insert)
from sounds import play_sound, make_sound_action

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
		"(dot|point)": Key('.'),
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

		"sing":    Key('squote'),
		"dub":     Key('dquote'),

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


def upper_first(text):
	if(len(text) > 1):
		return text[0].upper() + text[1:]
	elif(len(text) == 1):
		return text[0].upper()
	else:
		return text

def lower_first(text):
	if(len(text) > 1):
		return text[0].lower() + text[1:]
	elif(len(text) == 1):
		return text[0].lower()
	else:
		return text

fluid_insert_rule = MappingRule(
	name = "fluid insert base",
	mapping = {
		"say <text>":           Text("%(text)s"),
		"snake <snake_text>":   Text("%(snake_text)s") ,
		"camel <camel_text>":   Text("%(camel_text)s") ,
		"const <const_text>":   Text("%(const_text)s") ,
		"pascal <pascal_text>": Text("%(pascal_text)s") ,
		"lower <lower_text>":   Text("%(lower_text)s") ,
		"upper <upper_text>":   Text("%(upper_text)s") ,
		},
	extras = [
		Dictation("text"),
		Dictation("snake_text").lower().replace(" ", "_"),
		Dictation("const_text").upper().replace(" ", "_"),
		Dictation("camel_text").camel().apply(lower_first),
		Dictation("pascal_text").camel().apply(upper_first),
		Dictation("const_text").upper().replace(" ", "_"),
		Dictation("lower_text").lower(),
		Dictation("upper_text").upper(),
		],
)
fluid_insert = Optional(RuleRef(rule=fluid_insert_rule), name='fluid_insert')



def execute(obj):
	if not obj is None:
		obj.execute()

def execute_symbol_sequence(symbol_sequence, spaced=False):
	if not symbol_sequence is None:
		for symbol in symbol_sequence:
			symbol.execute()
			if(spaced):
				Key("space").execute()
		#if(spaced):
		#	Key("backspace").execute()

def build_rule(custom_symbol=Impossible()):

	symbol = Alternative(
		[RuleRef(rule=SymbolRule()), custom_symbol],
		name='symbol'
	)

	letter = RuleRef(rule=LetterRule(), name='letter')

	symbol_sequence = Optional(Repetition(
		Alternative([letter, symbol]),
		min=1, max=32
	), name='symbol_sequence')
	"""
	symbol_sequence = Sequence([
		Optional(Repetition(
			Alternative([letter, symbol]),
			min=1, max=32
		)),
		Optional(fluid_insert)
	], name='symbol_sequence')
	"""

	spell_rule = MappingRule(
		name = "letter mapping",
		mapping = {
			"press <symbol_sequence>": Function(execute_symbol_sequence),
			"spell <symbol_sequence> <fluid_insert>":
				Function(start_insert)
				  + Function(execute_symbol_sequence)
				  + Function(lambda fluid_insert: execute(fluid_insert))
				  + Function(end_insert),

			"trailing <symbol_sequence> <fluid_insert>":
				Function(start_insert)
				  + Function(execute_symbol_sequence, spaced=True)
				  + Function(lambda fluid_insert: execute(fluid_insert))
				  + Function(end_insert),

			"separate <symbol_sequence> <fluid_insert>":
				Function(start_insert)
				  + Function(execute_symbol_sequence, spaced=True)
				  + Key("backspace")
				  + Function(lambda fluid_insert: execute(fluid_insert))
				  + Function(end_insert),
	
#		# TODO Figure out how to bundle this into the rule below via defaults
#		#"<symbol>":
#		#	Function(start_insert)
#		#	  #+ Function(execute_symbol)
#		#	  + Function(lambda symbol: symbol.execute())
#		#	  + Function(end_insert),
#
			"<symbol> <symbol_sequence> <fluid_insert>":
				Function(start_insert)
				  + Function(lambda symbol: execute(symbol))
				  + Function(execute_symbol_sequence)
				  + Function(lambda fluid_insert: execute(fluid_insert))
				  + Function(end_insert),
			"<fluid_insert>":
				Function(start_insert)
				  + Function(lambda fluid_insert: execute(fluid_insert))
				  + Function(end_insert),
		},
		extras = [
			symbol_sequence,
			symbol,
			fluid_insert,
		],
	)

	return spell_rule
	


