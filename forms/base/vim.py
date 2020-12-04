from dragonfly import (Grammar, AppContext,
                       MappingRule, CompoundRule,
                       Dictation, Integer, Repeat,
					   IntegerRef, RuleRef,
					   Literal, Sequence, Repetition, Alternative,
                       Key, Text, Function, ActionBase)
from sounds import play_sound, make_sound_action

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
		"go to sleep": Key("npdiv"),
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
		"file write": Text(":w\n") + make_sound_action("write"),
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
		"window split horizontal": Key("c-w") + Key("s"),
		"window split vertical": Key("c-w") + Key("v"),

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

def set_mode_immediate(silent=False):
	set_mode(IMMEDIATE_MODE)
	if not silent:
		play_sound("mode imm")

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
	#global mode
	#global default_mode

	Key("escape").execute()
	#mode = default_mode
	set_mode(default_mode)

insert_rule = MappingRule(
	name = "insert",
	mapping = {
		"escape": Function(issue_escape) + make_sound_action("mode cmd"),

		"mode immediate": Function(set_mode_immediate),
		"mode insert":    Key("i") + Function(set_mode_immediate),
		"mode append":    Key("a") + Function(set_mode_immediate),
		"mode replace":   Key("R") + Function(set_mode_immediate),
		"mode search":    Key("slash") + Function(set_mode_immediate),

		"mode visual":       Key("v")   + make_sound_action("mode vis"),
		"mode visual line":  Key("V")   + make_sound_action("mode vis"),
		"mode visual block": Key("c-v") + make_sound_action("mode vis"),

		"default insert": Function(set_default_mode, new_mode=INSERT_MODE),
		"default append": Function(set_default_mode, new_mode=APPEND_MODE),

		"dictate": Function(start_insert) + Function(set_mode_immediate) + Key("cs-npmul"),

		# See fluid.py for the insertt rules


		# "[<n>] enter": Key("enter") * Repeat(extra="n"),

		"singles": Function(wrapped_insert, start = "'", end = "'"),
		"doubles": Function(wrapped_insert, start = '"', end = '"'),

		
        "[<n>] (line|lines) break":  Function(insert, action=Key("enter"), space=False)
		                              * Repeat(extra="n"),
		"insert line below": Key("o")   + Function(set_mode_immediate),
		"insert line above": Key("s-o") + Function(set_mode_immediate),

		"[<n>] backs":  Key("backspace") * Repeat(extra="n"),
		},
	extras = [

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
# See fluid.py

"""
========================================================================
= Edit rule
========================================================================
"""
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

edit_mapping = {
	"[<n>] undo": Text("%(n)s") + Key("u"),
	"[<n>] redo": Text("%(n)s") + Key("c-r"),

	"[<n>] (line|lines) join":   Text("%(n)s") + Key("s-j"),

	"[<n>] (line|lines) end delete": Text("%(n)s") + Key("s-d"),
	"[<n>] (line|lines) end change": Text("%(n)s") + Key("s-c"),

	"[<n>] paste (before|above)": Text("%(n)s") + Key("P"),
	"[<n>] paste (after|below)":  Text("%(n)s") + Key("p") + make_sound_action("paste"),
	
	"bracket match": Key("percent"),

	"repeat": Key("."),

	"[<n>] case (swap|toggle)": Text("%(n)s") + Key("~"),
}

edit_operands = {
	"(care|cares)": "l",
	"(term|terms)": "w",
	"(word|words)": "W",
	"(line|lines)": None,
	"(block|selection)": " "
}
for operand in edit_operands:
	edit_mapping.update({
		"[<n>] " + operand + " delete": Text("%(n)sd" + (edit_operands[operand] or "d"))
			+ make_sound_action("delete"),
		"[<n>] " + operand + " yank":   Text("%(n)sy" + (edit_operands[operand] or "y"))
			+ make_sound_action("yank"),
		"[<n>] " + operand + " change": Text("%(n)sc" + (edit_operands[operand] or "c"))
			+ Function(set_mode_immediate),
	})
	

edit_rule = MappingRule(
	name = "edit",
	mapping = edit_mapping,
	extras = [
		Integer("n", 1, 100),
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
	#grammar.add_rule(fluid.spell_rule)
	#grammar.add_rule(spell_rule)

	return grammar


