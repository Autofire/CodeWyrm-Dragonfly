from dragonfly import (Grammar,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, do_insert
from base import fluid

print("Loading grammar: bash")

kw_rules = {}

keywords = [
"git ",
"vim ",
"cargo ",
]

cargo_keywords = [
"build", "check", "clean",
"doc", "new", "init", 
"run", "test", "bench",     
"update", "search", "publish", "install", "uninstall"
]
for keyword in cargo_keywords:
	keywords += ["cargo " + keyword + " "]

git_keywords = [
"clone","init",
"add","reset",#"rm","mv",
"bisect","grep","log","show","status",
"branch","checkout","commit","diff","merge","rebase","tag",
"fetch","pull","push"
]
for keyword in git_keywords:
	keywords += ["git " + keyword + " "]

for keyword in keywords:
	kw_rules[keyword] = Text(keyword)

complex_words = {
"git move": "git mv ",
"git remove": "git rm ",

"list": "ls ",
"remove": "rm ",
"move": "mv ",
"cd": "cd ",
"copy": "cp ",

"as batch": "sbatch ",

"secure copy": "scp ",
"secure shell": "ssh ",

"Cal poly": "cpp",
"compute cluster": "hpc",
}
for word in complex_words:
	kw_rules[word] = Text(complex_words[word])

keyword_rule = MappingRule( name = "Bash keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("bash", context=(context))
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))  
	#grammar.add_rule(keyword_rule)  
	return grammar
