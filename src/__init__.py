import promptlayer

# load prompts here
SYSTEM_EXPLAIN = promptlayer.prompts.get("system_explain")['template']
SYSTEM_REFLECT = promptlayer.prompts.get("system_reflect")['template']
SYSTEM_COFFEECHAT = promptlayer.prompts.get("system_coffeechat")['template']
EXPLAIN = promptlayer.prompts.get("explain")['template']
SUGGEST = promptlayer.prompts.get("suggest")['template']


# define version here
__version__ = "0.0.4"
