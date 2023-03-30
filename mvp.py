"""
Just a quick implementation
"""
import os
from copy import deepcopy
from pprint import pprint

import gradio as gr
from pathlib import Path
from app.main import explain, log, chat, suggest
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
            book_dropdown = gr.Dropdown(["The Little Prince", "The Lord of the Flies", "Demian", "1984"],
                                        label="책 📚", multiselect=False)
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
                    txt = prince
                elif evt.value == "The Lord of the Flies":
                    txt = lord
                elif evt.value == "Demian":
                    txt = demian
                elif evt.value == "1984":
                    txt = _1984
                else:
                    raise gr.Error("Unknown book")
                return txt


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
                context = text[max(0, start - window_length):min(len(text), end + window_length)]
                d = explain(context, s_text)
                # 사용자에게 모든 프롬프트를 보여줄 필요는 없음.
                messages = deepcopy(d.messages[1:])  # noqa
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

            def after_response(s_text: str, d_raw: str):
                d = Dialogue.parse_raw(d_raw)
                suggestions = "\n".join(suggest("", s_text, d))
                return gr.update(value=suggestions, visible=True)

            def on_finish(s_text: str, d_raw: str):
                d = Dialogue.parse_raw(d_raw)
                log("", s_text, d)

        with gr.Column():
            chatbot = gr.Chatbot()
            prompt_area = gr.Text(placeholder="ask a follow-up and press Enter...",
                                  interactive=True, show_label=False, visible=False)
            suggest_area = gr.TextArea(interactive=False, visible=False, label="이런 질문은 어떤가요?")
            gr.Markdown(
                "> 모든 대화 기록은 [이 노션 페이지](https://www.notion.so/eubinecto/Vocabulary-Log-868b663485084b4cb502fc5741929419?pvs=4)에서"
                " 조회 가능합니다 🙂")
            # --- register listeners here --- #
            book_dropdown.select(on_select_dropdown, outputs=[text_area])
            text_area.select(on_select_area, outputs=[s_text_area, start_number, end_number])
            dialogue_area = gr.TextArea(visible=False)
            explain_button.click(lambda x: None,
                                 outputs=chatbot) \
                .then(on_click_explain,
                      inputs=[text_area, start_number, end_number],
                      outputs=[chatbot, dialogue_area, prompt_area]) \
                .then(after_response,
                      inputs=[s_text_area, dialogue_area],
                      outputs=suggest_area) \
                .then(on_finish,
                      inputs=[s_text_area, dialogue_area])
            prompt_area.submit(on_submit_prompt,
                               inputs=[s_text_area, dialogue_area, prompt_area],
                               outputs=[chatbot, dialogue_area, prompt_area]) \
                .then(lambda x: gr.update(visible=False),
                      outputs=suggest_area) \
                .then(on_finish,
                      inputs=[s_text_area, dialogue_area])
demo.launch(auth=(os.environ['NONSKIP_CLASSIC_USER'], os.environ['NONSKIP_CLASSIC_PASSWORD']))
