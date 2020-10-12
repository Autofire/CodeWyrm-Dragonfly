from dragonfly import (Grammar, AppContext, MappingRule, CompoundRule,
                       Dictation, IntegerRef, Integer, Repeat,
                       Key, Text, Function)

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

		"file write": Text(":w\n"),
		"file quit":  Text(":q\n"),

		"set line numbers": Text(":set nu! rnu!\n"),
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

		"page up":   Key("pageup"),
		"page down": Key("pagedown"),

		"bracket match": Key("percent"),
		},
	extras = [
		Integer("n", 1, 20),
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

def start_insert():
	global mode
	global default_mode

	if   mode == APPEND_MODE: Key("a").execute()
	elif mode == INSERT_MODE: Key("i").execute()

def end_insert():
	global mode
	Key("space").execute()

	if(mode != IMMEDIATE_MODE): 
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

		"say <text>":           Function(start_insert) + Text("%(text)s")        + Function(end_insert),
		"snake <snake_text>":   Function(start_insert) + Text("%(snake_text)s")  + Function(end_insert),
		"camel <camel_text>":   Function(start_insert) + Text("%(camel_text)s")  + Function(end_insert),
		"const <const_text>":   Function(start_insert) + Text("%(const_text)s")  + Function(end_insert),
		"pascal <pascal_text>": Function(start_insert) + Text("%(pascal_text)s") + Function(end_insert),

		"line [down] insert": Key("o")   + Function(set_mode_immediate),
		"line up insert":     Key("s-o") + Function(set_mode_immediate),

		"[<n>] backs":  Key("backspace") * Repeat(extra="n"),
		},
	extras = [
		Dictation("text"),
		Dictation("snake_text").lower().replace(" ", "_"),
		Dictation("const_text").upper().replace(" ", "_"),
		Dictation("camel_text").camel(),
		Dictation("pascal_text").camel().apply(upper_first),

		Integer("n", 1, 20),
		],
	defaults = {
		"n": 1,
		}
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

		"line end delete": Key("s-d"),

		"[<n>] (term|terms) delete": Text("%(n)s") + Key("d") + Key("w"),
		"[<n>] (term|terms) yank":   Text("%(n)s") + Key("y") + Key("w"),
		"[<n>] (term|terms) change": Text("%(n)s") + Key("c") + Key("w") + Function(set_mode_immediate),

		"[<n>] (word|words) delete": Text("%(n)s") + Key("d") + Key("W"),
		"[<n>] (word|words) yank":   Text("%(n)s") + Key("y") + Key("W"),
		"[<n>] (word|words) change": Text("%(n)s") + Key("c") + Key("W") + Function(set_mode_immediate),

		"[<n>] (line|lines) delete": Text("%(n)s") + Key("d") + Key("d"),
		"[<n>] (line|lines) yank":   Text("%(n)s") + Key("y") + Key("y"),
		"[<n>] (line|lines) change": Text("%(n)s") + Key("c") + Key("c") + Function(set_mode_immediate),

		"[<n>] paste (before|above)": Text("%(n)s") + Key("P"),
		"[<n>] paste (after|below)":  Text("%(n)s") + Key("p"),
		
		"bracket match": Key("percent"),

		"repeat": Key("."),
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
= Main grammar
========================================================================
"""
vimGrammar = Grammar("vim")
vimGrammar.add_rule(swallow_rule)
vimGrammar.add_rule(general_rule)
vimGrammar.add_rule(navi_rule)
vimGrammar.add_rule(edit_rule)
vimGrammar.add_rule(insert_rule)


"""
========================================================================
= Bootstrap grammar
========================================================================
"""
""" see https://stackoverflow.com/questions/58111733/modal-commands-with-dragonfly """
class VimEnabler(CompoundRule):
    spec = "dragon shift vim"

    def _process_recognition(self, node, extras): 
        vimBootstrap.disable()
        vimGrammar.enable()
        print "VIM grammar enabled"

class VimDisabler(CompoundRule):
    spec = "dragon revert vim"

    def _process_recognition(self, node, extras):
        vimGrammar.disable()
        vimBootstrap.enable()
        print "VIM grammar disabled"

vimBootstrap = Grammar("vim bootstrap")                
vimBootstrap.add_rule(VimEnabler())
vimGrammar.add_rule(VimDisabler())


vimGrammar.load()
vimBootstrap.load()

#vimGrammar.disable()
vimBootstrap.disable()

# Unload function which will be called by natlink at unload time.
def unload():
    global vimGrammar
    if vimGrammar: vimGrammar.unload()
    vimGrammar = None

    global vimBootstrap
    if vimBootstrap: vimBootstrap.unload()
    vimBootstrap = None
