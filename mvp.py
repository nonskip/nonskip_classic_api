"""
Just a quick implementation
"""
import json
from copy import deepcopy

import gradio as gr
from pathlib import Path
from app.main import explain, log, chat
from app.models import Dialogue

# 나중에 책으로 바꾸기.
with open(Path(__file__).resolve().parent / "assets" / "prince.txt") as fh:
    prince = fh.read()

with open(Path(__file__).resolve().parent / "assets" / "lord.txt") as fh:
    lord = fh.read()

with open(Path(__file__).resolve().parent / "assets" / "demian.txt") as fh:
    demian = fh.read()

with open(Path(__file__).resolve().parent / "assets" / "1984.txt") as fh:
    _1984 = fh.read()


with gr.Blocks() as demo:
    gr.Markdown("## Nonskip Classic 📜 (MVP)")
    gr.Markdown("> Don't skip a single word you don't understand.")
    with gr.Row():
        with gr.Column(scale=10):
            dropdown = gr.Dropdown(["The Little Prince", "The Lord of the Flies", "Demian", "1984"],
                                   label="책 📚")
            text_area = gr.TextArea(interactive=False, label="책 원문")
            s_text_area = gr.TextArea(interactive=False, label="선택한 텍스트")
            start_number = gr.Number(visible=False)
            end_number = gr.Number(visible=False)
            explain_button = gr.Button("explain")

            def on_select_dropdown(evt: gr.SelectData) -> str:
                """
                Get the selected text
                """
                if evt.value == "The Little Prince":
                    return prince
                elif evt.value == "The Lord of the Flies":
                    return lord
                elif evt.value == "Demian":
                    return demian
                elif evt.value == "1984":
                    return _1984
                else:
                    raise gr.Error("Unknown book")

            def on_select_area(evt: gr.SelectData) -> tuple[str, int, int]:
                """
                Get the selected text
                """
                return evt.value, evt.index[0], evt.index[1]

            def on_click_explain(text: str, start: int, end: int):
                """
                Explain the selected text
                """
                start = int(start)
                end = int(end)
                s_text = text[start:end]
                if len(s_text) == 0:
                    raise gr.Error("Please select a text first")
                window_length = 500
                context = text[max(0, start-window_length):min(len(text), end+window_length)]
                d = explain(context, s_text)
                messages = deepcopy(d.messages[1:])  # the first one is a system message. so we don't need it
                messages[0].content = s_text
                evens = [m.content for m in messages[0::2]]
                odds = [m.content for m in messages[1::2]]
                history = list(zip(evens, odds))
                return history, d.json(), gr.update(visible=True)

            def on_submit_prompt(s_text: str, d_raw: str, prompt: str):
                d = Dialogue.parse_raw(d_raw)
                d = chat(prompt, d)
                messages = deepcopy(d.messages[1:])  # the first one is a system message. so we don't need it
                messages[0].content = s_text
                evens = [m.content for m in messages[0::2]]
                odds = [m.content for m in messages[1::2]]
                history = list(zip(evens, odds))
                return history, d.json(), None

            def on_finish(s_text: str, d_raw: str):
                d = Dialogue.parse_raw(d_raw)
                log("", s_text, d)

        with gr.Column():
            chatbot = gr.Chatbot()
            prompt_area = gr.Text(placeholder="ask a follow-up and press Enter...",
                                  interactive=True, show_label=False, visible=False)
            # --- register listeners here --- #
            dropdown.select(on_select_dropdown, outputs=text_area)
            text_area.select(on_select_area, outputs=[s_text_area, start_number, end_number])
            dialogue_area = gr.TextArea(visible=False)
            explain_button.click(lambda x: None,
                                 outputs=chatbot)\
                          .then(on_click_explain,
                                inputs=[text_area, start_number, end_number],
                                outputs=[chatbot, dialogue_area, prompt_area])\
                          .then(on_finish,
                                inputs=[s_text_area, dialogue_area])
            prompt_area.submit(on_submit_prompt,
                               inputs=[s_text_area, dialogue_area, prompt_area],
                               outputs=[chatbot, dialogue_area, prompt_area])\
                       .then(on_finish,
                             inputs=[s_text_area, dialogue_area])
demo.launch(share=True)
