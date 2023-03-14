import readpilot as rp


def explain(text: str, h_text: str) -> rp.Dialogue:
    """
    Explain the highlighted text in the text.
    :param text: the text to be explained.
    :param h_text: the highlighted text to be explained.
    :return: a Dialogue object.
    """
    # create a prompt out of the text and the highlighted text.
    prompt = rp.prompts.PROMPT_EXPLAIN.format(text=text, h_text=h_text)
    d = rp.chat(prompt, rp.Dialogue(text=text, h_text=h_text))
    return d

