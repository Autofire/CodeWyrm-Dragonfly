from dragonfly import (Grammar, AppContext,
                       MappingRule, CompoundRule,
                       Dictation, Integer, Repeat,
					   IntegerRef, RuleRef,
					   Literal, Sequence, Repetition, Alternative,
                       Key, Text, Function)

print("Loading grammar: vim")

"""
========================================================================
= Swallow rule
========================================================================
"""
swallow_rule = MappingRule(
	name = "swallow",
	mapping = {
		"<text>": Text(""),
		},
	extras = [
		Dictation("text"),
		],
)


"""
========================================================================
= General rule
========================================================================
"""
general_rule = MappingRule(
	name = "general",
	mapping = {

		"file first": Text(":first\n"),
		"file next": Text(":n\n"),
		"file previous": Text(":N\n"),
		"file last": Text(":last\n"),

		"all (file|files) write": Text(":wa\n"),
		"file write": Text(":w\n"),
		"file force write": Text(":w!"),

		"file quit":  Text(":q\n"),
		"file force quit":  Text(":q!"),

		"set line numbers": Text(":set nu! rnu!\n"),

		},
	extras = [
		Dictation("text"),
		],
)

"""
========================================================================
= Window rule
========================================================================
"""
window_rule = MappingRule(
	name = "window",
	mapping = {
		"window row split": Key("c-w") + Key("s"),
		"window column split": Key("c-w") + Key("v"),

		"window up": Key("c-w") + Key("up"),
		"window down": Key("c-w") + Key("down"),
		"window left": Key("c-w") + Key("left"),
		"window right": Key("c-w") + Key("right"),
				
		},
	extras = [
		Dictation("text"),
		],
)

"""
========================================================================
= Navi rule
========================================================================
"""
navi_rule = MappingRule(
	name = "navi",
	mapping = {
		"[<n>] (line|lines) up":    Key("up")    * Repeat(extra="n"),
		"[<n>] (line|lines) down":  Key("down")  * Repeat(extra="n"),

		"[<n>] (care|cares) right": Key("right") * Repeat(extra="n"),
		"[<n>] (care|cares) left":  Key("left")  * Repeat(extra="n"),


		"[<n>] (term|terms) right": Text("%(n)s") + Key("w"),
		"[<n>] (term|terms) left":  Text("%(n)s") + Key("b"),
		"[<n>] (word|words) right": Text("%(n)s") + Key("W"),
		"[<n>] (word|words) left":  Text("%(n)s") + Key("B"),

		"[<n>] (end|ends) right":   Text("%(n)s") + Key("e"),
		"[<n>] (end|ends) left":    Text("%(n)s") + Text("ge"),
		"[<n>] (tail|tails) right": Text("%(n)s") + Key("E"),
		"[<n>] (tail|tails) left":  Text("%(n)s") + Text("gE"),

		"line top":    Text("gg"),
		"line <abs>":  Text("%(abs)s") + Text("gg"),
		"line bottom": Text("G"),

		"line end":   Key("dollar"),
		"line start": Key("caret"),
		"line awake": Key("0"),

		"[<n>] (page|pages) up":   Text("%(n)s") + Key("pgup"),
		"[<n>] (page|pages) down": Text("%(n)s") + Key("pgdown"),

		"bracket match": Key("percent"),
		},
	extras = [
		Integer("n", 1, 200),
		Integer("abs", 1, 20000),
		Dictation("text"),
		],
	defaults = {
		"n": 1,
		"abs": 1
		}
)


"""
========================================================================
= Insertion rule
========================================================================
"""
IMMEDIATE_MODE = -1
APPEND_MODE = 0
INSERT_MODE = 1

default_mode = APPEND_MODE
mode = default_mode
def set_mode(new_mode):
	global mode
	mode = new_mode

def set_mode_immediate():
	set_mode(IMMEDIATE_MODE)

def set_default_mode(new_mode):
	global default_mode
	default_mode = new_mode
	set_mode(new_mode)

def insert(action, space=False):
	start_insert()
	action.execute()
	end_insert(space)

def wrapped_insert(start, end):
	start_insert()
	set_mode_immediate()
	Text(start + end).execute()
	Key("left:" + str(len(end))).execute()

def do_insert(text):
	return Function(insert, action=Text(text))

def start_insert():
	global mode
	global default_mode

	if   mode == APPEND_MODE: Key("a").execute()
	elif mode == INSERT_MODE: Key("i").execute()

def end_insert(space=False):
	global mode

	if(mode != IMMEDIATE_MODE): 
		if(space): 
			Key("space").execute()
		issue_escape()

def issue_escape():
	global mode
	global default_mode

	Key("escape").execute()
	mode = default_mode

def upper_first(text):
	if(len(text) > 1):
		return text[0].upper() + text[1:]
	elif(len(text) == 1):
		return text[0].upper()
	else:
		return text

insert_rule = MappingRule(
	name = "insert",
	mapping = {
		"escape": Function(issue_escape),

		"mode insert":  Key("i") + Function(set_mode_immediate),
		"mode append":  Key("a") + Function(set_mode_immediate),
		"mode replace": Key("R") + Function(set_mode_immediate),

		"default insert": Function(set_default_mode, new_mode=INSERT_MODE),
		"default append": Function(set_default_mode, new_mode=APPEND_MODE),

		"say <text>":           Function(start_insert)
		                         + Text("%(text)s")
								 + Function(end_insert),
		"snake <snake_text>":   Function(start_insert)
		                         + Text("%(snake_text)s")
								 + Function(end_insert),
		"camel <camel_text>":   Function(start_insert)
		                         + Text("%(camel_text)s")
								 + Function(end_insert),
		"const <const_text>":   Function(start_insert)
		                         + Text("%(const_text)s")
								 + Function(end_insert),
		"pascal <pascal_text>": Function(start_insert)
		                         + Text("%(pascal_text)s")
								 + Function(end_insert),
		"lower <lower_text>": Function(start_insert)
		                         + Text("%(lower_text)s")
								 + Function(end_insert),
		"upper <upper_text>": Function(start_insert)
		                         + Text("%(upper_text)s")
								 + Function(end_insert),
		"num <posVal>":         Function(start_insert)
		                         + Text("%(posVal)s")
								 + Function(end_insert),


		"[<n>] slap": Key("enter") * Repeat(extra="n"),

		"singles": Function(wrapped_insert, start = "'", end = "'"),
		"doubles": Function(wrapped_insert, start = '"', end = '"'),

		
        "[<n>] (line|lines) break":  Function(insert, action=Key("enter"), space=False)
		                              * Repeat(extra="n"),
		"line insert below": Key("o")   + Function(set_mode_immediate),
		"line insert above": Key("s-o") + Function(set_mode_immediate),

		"[<n>] backs":  Key("backspace") * Repeat(extra="n"),
		},
	extras = [
		Dictation("text"),
		Dictation("snake_text").lower().replace(" ", "_"),
		Dictation("const_text").upper().replace(" ", "_"),
		Dictation("camel_text").camel(),
		Dictation("pascal_text").camel().apply(upper_first),
		Dictation("const_text").upper().replace(" ", "_"),
		Dictation("lower_text").lower(),
		Dictation("upper_text").upper(),

		Integer("n", 1, 20),
		Integer("posVal", 0, 1000),
		],
	defaults = {
		"n": 1,
		}
)


"""
========================================================================
= Spell rule
========================================================================
"""
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

		"(minus|dash)":   Key("minus"),
		"plus":           Key("plus"),
		"(slash|divide)": Key("slash"),
		"(star|times)":   Key("star"),

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
	}

letter_names = [
	'ash', 'bug', 'chip', 'dog', 'egg', 'flame',
	'giga', 'hub', 'ice', 'jack', 'king', 'lash',
	'mule', 'net', 'oak', 'page', 'quail', 'raft',
	'scout', 'tide', 'use', 'vast', 'whale', 'x-ray',
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

symbol = RuleRef(rule=SymbolRule(), name='symbol')
letter = RuleRef(rule=LetterRule(), name='letter')
letter_sequence = Repetition(
	Alternative([letter, symbol]),
	min=1, max=32, name='letter_sequence'
)

def execute_symbol(symbol):
    symbol.execute()

def execute_letter(letter):
    letter.execute()

def execute_letter_sequence(letter_sequence):
    for letter in letter_sequence:
        letter.execute()

spell_rule = MappingRule(
	name = "letter mapping",
	mapping = {
		"press <letter_sequence>": Function(execute_letter_sequence),
		"spell <letter_sequence>":
			Function(start_insert)
			  + Function(execute_letter_sequence)
			  + Function(end_insert),

		# TODO Figure out how to bundle this into the rule below via defaults
		"<symbol>":
			Function(start_insert)
		      + Function(execute_symbol)
			  + Function(end_insert),

		"<symbol> <letter_sequence>":
			Function(start_insert)
		      + Function(execute_symbol)
		      + Function(execute_letter_sequence)
			  + Function(end_insert),
	},
	extras = [
		letter_sequence,
		symbol
	],
)

"""
========================================================================
= Edit rule
========================================================================
"""
edit_rule = MappingRule(
	name = "edit",
	mapping = {
		"[<n>] undo": Text("%(n)s") + Key("u"),
		"[<n>] redo": Text("%(n)s") + Key("c-r"),


		"[<n>] (care|cares) delete": Text("%(n)s") + Text("dl"),
		"[<n>] (care|cares) yank":   Text("%(n)s") + Text("yl"),
		"[<n>] (care|cares) change": Text("%(n)s") + Text("cl")
			+ Function(set_mode_immediate),

		"[<n>] (term|terms) delete": Text("%(n)s") + Text("dw"),
		"[<n>] (term|terms) yank":   Text("%(n)s") + Text("yw"),
		"[<n>] (term|terms) change": Text("%(n)s") + Text("cw")
			+ Function(set_mode_immediate),

		"[<n>] (word|words) delete": Text("%(n)s") + Text("dW"),
		"[<n>] (word|words) yank":   Text("%(n)s") + Text("yW"),
		"[<n>] (word|words) change": Text("%(n)s") + Text("cW")
			+ Function(set_mode_immediate),

		"[<n>] (line|lines) delete": Text("%(n)s") + Text("dd"),
		"[<n>] (line|lines) yank":   Text("%(n)s") + Text("yy"),
		"[<n>] (line|lines) change": Text("%(n)s") + Text("cc")
			+ Function(set_mode_immediate),
		"[<n>] (line|lines) join":   Text("%(n)s") + Key("s-j"),
		"line end delete": Key("s-d"),

		"[<n>] paste (before|above)": Text("%(n)s") + Key("P"),
		"[<n>] paste (after|below)":  Text("%(n)s") + Key("p"),
		
		"bracket match": Key("percent"),

		"repeat": Key("."),

		"[<n>] case toggle": Text("%(n)s") + Key("~"),
		},
	extras = [
		Integer("n", 1, 20),
		Dictation("text"),
		],
	defaults = {
		"n": 1,
		}
)


"""
========================================================================
= Help grammar
========================================================================
"""



"""
========================================================================
= Main grammar
========================================================================
"""
def build_grammar(context):
	grammar = Grammar("vim", context=(context))
	grammar.add_rule(swallow_rule)
	grammar.add_rule(general_rule)
	grammar.add_rule(navi_rule)
	grammar.add_rule(edit_rule)
	grammar.add_rule(insert_rule)
	grammar.add_rule(window_rule)
	grammar.add_rule(spell_rule)
	return grammar


"""
========================================================================
= Bootstrap grammar
========================================================================
"""
""" see https://stackoverflow.com/questions/58111733/modal-commands-with-dragonfly """

"""
class VimEnabler(CompoundRule):
    spec = "dragon shift vim"

    def _process_recognition(self, node, extras): 
        vimBootstrap.disable()
        grammar.enable()
        print "VIM grammar enabled"

class VimDisabler(CompoundRule):
    spec = "dragon revert vim"

    def _process_recognition(self, node, extras):
        grammar.disable()
        vimBootstrap.enable()
        print "VIM grammar disabled"

vimBootstrap = Grammar("vim bootstrap")                
vimBootstrap.add_rule(VimEnabler())
grammar.add_rule(VimDisabler())


grammar.load()
vimBootstrap.load()

#grammar.disable()
vimBootstrap.disable()
"""

#grammar.load()

# Unload function which will be called by natlink at unload time.
"""
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None


global vimBootstrap
if vimBootstrap: vimBootstrap.unload()
vimBootstrap = None
"""
