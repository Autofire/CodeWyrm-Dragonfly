from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef,
                       Key, Text)

print("Loading grammar: bash")

"""
git_context = AppContext(title="git Bash")
git_context2 = AppContext(title="MINGW32:")
# set the window title to bash in putty for this context to work
putty_context = AppContext(title="bash")
extraterm_context = AppContext(executable="extraterm")
grammar = Grammar(
	"bash", 
	context=(
		putty_context 
		| git_context 
		| git_context2 
		| extraterm_context))
"""

file_extensions_rule = MappingRule(
	name = "file extensions",
	mapping = {
		"dot text": Text(".txt"),
		"dot pie": Text(".py"),
		"dot rust": Text(".rs"),
		"dot C. P. P.": Text(".cpp"),
		"dot C.": Text(".c"),
		},
	extras = [
		],
)


bash_rule = MappingRule(
	name = "bash",
	mapping = {
		"P. W. D.": Text("pwd\n"),

		"dot dot": Text("../"),

		"CD dot dot": Text("cd ..\n"),
		"CD double dot": Text("cd ..\n"),
		"CD triple dot": Text("cd ../..\n"),
		"CD ": Text("cd ") + Key("tab:3"),
		"CD <text>": Text("cd %(text)s"),

		"copy": Text("cp "),
		"copy <text>": Text("cp %(text)s"),

		"make directory ": Text("mkdir "),
		"make directory <text>": Text("mkdir %(text)s\n"),

		"move": Text("mv "),
		"move <text>": Text("mv %(text)s"),
		"remove": Text("rm "),
		"remove <text>": Text("rm %(text)s"),

		"secure copy": Text("scp"),
		"secure copy <text>": Text("scp %(text)"),

		"change mode": Text("chmod "),

		"grep <text>": Text("grep %(text)s"),

		"cat": Text("cat "),
		"cat <text>": Text("cat %(text)s"),
		"exit": Text("exit\n"),

		"list": Text("ls\n"),
		"list <text>": Text("ls %(text)s"),
		"list minus L.": Text("ls -l\n"),
		"list minus A.": Text("ls -a\n"),
		"list minus one": Text("ls -1 "),

		"pipe": Text(" | "),

		"D. P. K. G. ": Text("dpkg "),
		"D. P. K. G. minus L.": Text("dpkg -l "),
		"D. P. K. G. minus I.": Text("dpkg -i "),

		"man": Text("man "),

		"word count": Text("wc "),
		"word count minus L.": Text("wc -l "),

		"touch": Text("touch "),

		"repeat previous arg": Key("a-dot"),
		"up": Key("up"),

		# cursor movement
		"back": Key("a-b"),
		"[<n>] back": Key("a-b:%(n)d"),
		"[<n>] whiskey": Key("a-f:%(n)d"),
		"dollar": Key("c-e"),
		"hat": Key("c-a"),

		"scratch": Key("c-w"),
		"[<n>] scratch": Key("c-w:%(n)d"),
		"paste": Key("c-y"),

		"make": Text("make\n"),
		"make clean": Text("make clean\n"),

		"evince": Text("evince "),
		"evince <text>": Text("evince %(text)s"),

                "Python": Text("python "),

		"aptitude search": Text("aptitude search "),
		"pseudo-aptitude install": Text("sudo aptitude install "),
		"pseudo-aptitude update": Text("sudo aptitude update "),
		"pseudo-aptitude remove": Text("sudo aptitude remove "),

		"A. P. T. file search": Text("apt-file search "),

		"vim": Text("vim "),
		"vim <text>": Text("vim %(text)s"),


		"W. get ": Text("wget "),

		"cancel": Key("c-c"),
		},
	extras = [
		Dictation("text"),
		IntegerRef("n", 1, 20)
		],
	defaults = {
		"n": 1
	}
)


git_rule = MappingRule(
	name = "git",
	mapping = {
		# commands for git version control
		"get add": Text("git add "),
		"get add <text>": Text("git add %(text)s"),
		"get remove": Text("git rm "),
		"get remove <text>": Text("git rm %(text)s"),
		"get move": Text("git move "),
		"get move <text>": Text("git mv %(text)s"),
		"get status": Text("git status\n"),
		"get patch": Text("git add -p\n"),

		"get branch": Text("git branch "),

		"get merge": Text("git merge "),
		"get merge not fast forward": Text("git merge --no-ff "),

		"get log": Text("git log\n"),
		"get log [color] words": Text("git log -p --color-words\n"),
		"get log minus (P.|patch)": Text("git log -p\n"),
		"get log minus stat": Text("git log --stat\n"),

		"get diff": Text("git diff\n"),
		"get diff [color] words": Text("git diff --color-words\n"),
		"get diff cache": Text("git diff --cached\n"),
		"get diff [color] words cached": Text("git diff --color-words --cached\n"),


		"get submodule init": Text("git submodule init "),
		"get submodule update": Text("git submodule update "),

		"get kay": Text("gitk\n"),
		"get kay all": Text("gitk --all\n"),

		"get commit message": Text("git commit -m ''") + Key("left"),
		"get commit": Text("git commit "),
		"get commit --amend": Text("git commit --amend\n"),

		"get check out": Text("git checkout "),
		"get check out <text>": Text("git checkout %(text)s"),
		"get check out minus F.": Text("git checkout -f\n"),

		"get stash": Text("git stash\n"),

		"get pull": Text("git pull\n"),
		"get clone": Text("git clone ") + Key("cs-v"),

		"get push": Text("git push\n"),
		"get help": Text("git help"),
		"get help push": Text("git help push\n"),

		"get remote add": Text("git remote add"),
		"yes": Key("y,enter"),
		"no": Key("n,enter"),
		"quit": Key("q,enter"),
		},
	extras = [
		Dictation("text"),
		],
)

prefix_key = "c-a"

screen_rule = MappingRule(
	name = "screen",
	mapping = {
		"switch to (screen | window) <n>": Key(prefix_key) + Key("%(n)d"),
		"switch to (window next | next window | screen next | next screen)":
			Key(prefix_key) + Key("n"),
		"switch to (window previous | previous window | screen previous | previous screen)":
			Key(prefix_key) + Key("p"),
		"create (screen | window)": Key(prefix_key) + Key("c"),
		},
	extras = [
		IntegerRef("n", 0, 20)
		]
)

def build_grammar(context):
	grammar = Grammar("bash", context=(context))
	grammar.add_rule(file_extensions_rule)
	grammar.add_rule(bash_rule)
	#grammar.add_rule(screen_rule)
	grammar.add_rule(git_rule)
	#grammar.load()
	return grammar

# Unload function which will be called by natlink at unload time.
"""
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
"""

