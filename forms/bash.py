from dragonfly import (Grammar,
                       MappingRule, CompoundRule,
                       Dictation, Key, Text, Function)
from vim import wrapped_insert, insert, do_insert

print("Loading grammar: bash")

kw_rules = {}

keywords = [
"git ",
"vim ",
]
for keyword in keywords:
	kw_rules[keyword] = do_insert(keyword)

complex_words = {
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
	kw_rules[word] = do_insert(complex_words[word])

keyword_rule = MappingRule( name = "Bash keywords", mapping = kw_rules )

def build_grammar(context):
	grammar = Grammar("bash", context=(context))
	grammar.add_rule(keyword_rule)  
	return grammar
