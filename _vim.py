from dragonfly import (Grammar, AppContext, MappingRule, CompoundRule,
                       Dictation, IntegerRef, Integer,
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
		"escape": Key("escape"),

		"undo": Key("u"),
		"redo": Key("c-r"),

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
		"[<n>] (line|lines) up":    Text("%(n)s") + Key("k"),
		"[<n>] (line|lines) down":  Text("%(n)s") + Key("j"),

		"[<n>] (care|cares) right": Text("%(n)s") + Key("l"),
		"[<n>] (care|cares) left":  Text("%(n)s") + Key("h"),

		"[<n>] (byte|bytes) right": Text("%(n)s") + Key("w"),
		"[<n>] (byte|bytes) left":  Text("%(n)s") + Key("b"),
		"[<n>] (word|words) right": Text("%(n)s") + Key("W"),
		"[<n>] (word|words) left":  Text("%(n)s") + Key("B"),

		"[<n>] (end|ends) right":   Text("%(n)s") + Key("e"),
		"[<n>] (end|ends) left":    Text("%(n)s") + Text("ge"),
		"[<n>] (tail|tails) right": Text("%(n)s") + Key("E"),
		"[<n>] (tail|tails) left":  Text("%(n)s") + Text("gE"),

		"top line":    Text("gg"),
		"<abs> line":  Text("%(abs)s") + Text("gg"),
		"bottom line": Text("G"),

		"line end":   Key("dollar"),
		"line start": Key("caret"),
		"line zero":  Key("0"),

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
= Edit rule
========================================================================
"""
edit_rule = MappingRule(
	name = "edit",
	mapping = {
		"[<n>] (line|lines) delete": Text("%(n)s") + Key("d") + Key("d"),
		"[<n>] (line|lines) yank":   Text("%(n)s") + Key("y") + Key("y"),

		"[<n>] (byte|bytes) delete": Text("%(n)s") + Key("d") + Key("w"),
		"[<n>] (byte|bytes) yank":   Text("%(n)s") + Key("y") + Key("w"),
		"[<n>] (word|words) delete": Text("%(n)s") + Key("d") + Key("W"),
		"[<n>] (word|words) yank":   Text("%(n)s") + Key("y") + Key("W"),


		"bracket match": Key("percent"),
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
= Insertion rule
========================================================================
"""
NONE_MODE = -1
APPEND_MODE = 0
INSERT_MODE = 1

default_mode = APPEND_MODE
mode = default_mode
def set_mode(new_mode):
	global mode
	mode = new_mode

def set_default_mode(new_mode):
	global default_mode
	default_mode = new_mode
	set_mode(new_mode)

def insert_action():
	global mode
	global default_mode

	if   mode == APPEND_MODE: Key("a").execute()
	elif mode == INSERT_MODE: Key("i").execute()

	mode = default_mode

insert_rule = MappingRule(
	name = "insert",
	mapping = {
		"mode insert": Function(set_default_mode, new_mode=INSERT_MODE),
		"mode append": Function(set_default_mode, new_mode=APPEND_MODE),

		"say <text>":         Function(insert_action) + Text("%(text)s")       + Key("escape"),
		"snake <snake_text>": Function(insert_action) + Text("%(snake_text)s") + Key("escape"),
		"camel <camel_text>": Function(insert_action) + Text("%(camel_text)s") + Key("escape"),
		"const <const_text>": Function(insert_action) + Text("%(const_text)s") + Key("escape"),

		"insert line":       Key("o")   + Function(set_mode, new_mode=NONE_MODE),
		"insert line above": Key("s-o") + Function(set_mode, new_mode=NONE_MODE),
		},
	extras = [
		Dictation("text"),
		Dictation("snake_text").lower().replace(" ", "_"),
		Dictation("const_text").upper().replace(" ", "_"),
		Dictation("camel_text").camel()
		],
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
