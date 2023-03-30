import promptlayer

# load prompts here
SYSTEM = promptlayer.prompts.get("system")['template']
EXPLAIN = promptlayer.prompts.get("explain")['template']
SUGGEST = promptlayer.prompts.get("suggest")['template']


# define version here
__version__ = "0.0.3"
