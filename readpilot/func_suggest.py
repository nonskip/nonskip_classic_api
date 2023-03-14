from .model_dialogue import Dialogue
from .func_chat import chat
from .prompts import PROMPT_SUGGEST


def suggest(d: Dialogue) -> list[str]:
    d = chat(PROMPT_SUGGEST, d)
    suggestions = d.messages[-1].content.split('\n')
    return suggestions
