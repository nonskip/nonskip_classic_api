from pprint import pprint
import promptlayer

# get prompts from promptlayer and have a quick look of them
SYSTEM = promptlayer.prompts.get("system")
pprint(SYSTEM)
print("------")

EXPLAIN = promptlayer.prompts.get("explain")
pprint(EXPLAIN)
print("------")

SUGGEST = promptlayer.prompts.get("suggest")
pprint(SUGGEST)
print("------")
