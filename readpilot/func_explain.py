from . import Dialogue, chat


def explain(text: str, h_text: str) -> Dialogue:
    """
    Explain the highlighted text in the text.
    :param text: the text to be explained.
    :param h_text: the highlighted text to be explained.
    :return: a Dialogue object.
    """
    # create a prompt out of the text and the highlighted text.
    prompt = ...
    d = Dialogue(text=text, h_text=h_text)
    #d = chat(d, prompt)
    return d

