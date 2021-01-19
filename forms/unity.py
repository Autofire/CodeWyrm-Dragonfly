from dragonfly import (Grammar, Alternative,
                       MappingRule, CompoundRule, RuleRef,
                       Dictation, Key, Text, Function)
from base.vim import wrapped_insert, insert, Text
from base import fluid
import cs

print("Loading grammar: unity")

kw_rules = {}

keywords = [
"Vector3", "Vector2", "Vector4",
"GameObject", "Tranform", "RectTransform",
"Mathf",
]
for keyword in keywords:
	kw_rules[keyword] = Text(keyword)

complex_kw = {
	"local GameObject": "gameobject",
	"local transform": "transform",
	"arguments": "args",
}
for key in complex_kw:
	kw_rules[key] = Text(complex_kw[key])

kw_rules.update(cs.get_keyword_rules())
keyword_rule = MappingRule( name = "unity keywords", mapping = kw_rules )

def build_grammar(context):
	#grammar = cs.build_grammar(context, "unity")
	grammar = Grammar("unity", context=(context))
	grammar.add_rule(fluid.build_rule(RuleRef(rule=keyword_rule)))
	return grammar
