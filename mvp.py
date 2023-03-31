"""
Just a quick implementation
"""
from copy import deepcopy
import gradio as gr
from pathlib import Path
from app.main import explain, log, chat, suggest
from app.models import Dialogue
import textwrap

# --- constants --- #
MAX_PAGE_CHARS = 1000

# --- loading books here --- #
with open(Path(__file__).resolve().parent / "assets" / "prince.txt") as fh:
    prince_pages = textwrap.wrap(fh.read(), MAX_PAGE_CHARS, replace_whitespace=False)

with open(Path(__file__).resolve().parent / "assets" / "lord.txt") as fh:
    lord_pages = textwrap.wrap(fh.read(), MAX_PAGE_CHARS, replace_whitespace=False)

with open(Path(__file__).resolve().parent / "assets" / "demian.txt") as fh:
    demian_pages = textwrap.wrap(fh.read(), MAX_PAGE_CHARS, replace_whitespace=False)

with open(Path(__file__).resolve().parent / "assets" / "1984.txt") as fh:
    _1984_pages = textwrap.wrap(fh.read(), MAX_PAGE_CHARS, replace_whitespace=False)

books = {
    'The Little Prince': {
        'pages': prince_pages,
    },
    'The Lord of the Flies': {
        'pages': lord_pages,
    },
    'Demian': {
        'pages': demian_pages,
    },
    '1984': {
        'pages': _1984_pages,
    }
}

with gr.Blocks(theme=gr.themes.Monochrome()) as interface:
    # ---- variables ---- #
    curr_page = gr.Number(visible=False)  # store current page here
    start_number = gr.Number(visible=False)  # s_text start number
    end_number = gr.Number(visible=False)  # s_text end number

    # --- start rendering from here --- #
    gr.Markdown("# Nonskip Classic 📜 (MVP)")
    with gr.Row():
        with gr.Column(scale=20):
            with gr.Group():
                titles_dropdown = gr.Dropdown(list(books.keys()), label="📚classics", multiselect=False)
                title_text = gr.Text(visible=False)
                text_area = gr.TextArea(interactive=False, label="📖text")
        with gr.Column():
            with gr.Row():
                with gr.Group(equal_width=True):
                    # put all the buttons side by side
                    prev_button = gr.Button("◀️")
                    curr_button = gr.Button("(.../...)", interactive=False)
                    next_button = gr.Button("▶️")
                    flag_button = gr.Button("flag")
                    explain_button = gr.Button("explain")
                    s_text_area = gr.Textbox(interactive=False, label="🪞selected")
                    flags_dropdown = gr.Dropdown(label="🚩flags", multiselect=True)

                with gr.Group():
                    chatbot = gr.Chatbot(label="ChatGPT")
                    prompt_area = gr.Text(placeholder="ask a follow-up and press Enter...",
                                          interactive=True, show_label=False, visible=False)
                    suggest_area = gr.TextArea(interactive=False, visible=False, label="이런 질문은 어떤가요?")
                    gr.Markdown(
                        "> 모든 대화 기록은 [이 노션 페이지](https://www.notion.so/eubinecto/"
                        "Vocabulary-Log-868b663485084b4cb502fc5741929419?pvs=4)에서"
                        " 조회 가능합니다 🙂", visible=False)


                def update_curr_page(page: int, title: str):
                    page = int(page)
                    max_page = len(books[title]['pages'])
                    return f"({page + 1}/{max_page})"


                def on_select_text_area(evt: gr.SelectData) -> tuple[str, int, int]:
                    """
                    Get the selected text
                    """
                    return evt.value, evt.index[0], evt.index[1]


                def on_click_flag_button(flags: list[str], s_text: str, start: int):
                    start = int(start)
                    flags.append(f"{s_text}🏷{start}")
                    return flags


                def on_click_explain_button(text: str, start: int, end: int):
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


                def on_submit_prompt_area(s_text: str, d_raw: str, prompt: str):
                    d = Dialogue.parse_raw(d_raw)
                    prompt = "(문맥 상) " + prompt
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


                def on_click_prev_button(page: int, title: str):
                    page = int(page)
                    page -= 1
                    page = max(0, page)
                    return page, books[title]['pages'][page]


                def on_click_next_button(page: int, title: str):
                    page = int(page)
                    page += 1
                    page = min(len(books[title]['pages']) - 1, page)
                    return page, books[title]['pages'][page]


                # --- register listeners here --- #
                titles_dropdown.select(lambda x: x, inputs=titles_dropdown, outputs=title_text) \
                    .then(lambda x: books[x]['pages'][0], inputs=title_text, outputs=text_area) \
                    .then(lambda x: 0, outputs=curr_page) \
                    .then(lambda x: list(), outputs=flags_dropdown) \
                    .then(update_curr_page, inputs=[curr_page, title_text], outputs=curr_button)
                text_area.select(on_select_text_area,
                                 outputs=[s_text_area, start_number, end_number])
                dialogue_area = gr.TextArea(visible=False)
                prev_button.click(on_click_prev_button, inputs=[curr_page, title_text], outputs=[curr_page, text_area]) \
                    .then(update_curr_page, inputs=[curr_page, title_text], outputs=curr_button)\
                    .then(lambda x: None, outputs=s_text_area)\
                    .then(lambda x: list(), outputs=flags_dropdown)
                next_button.click(on_click_next_button, inputs=[curr_page, title_text], outputs=[curr_page, text_area]) \
                    .then(update_curr_page, inputs=[curr_page, title_text], outputs=curr_button) \
                    .then(lambda x: None, outputs=s_text_area) \
                    .then(lambda x: list(), outputs=flags_dropdown)
                flag_button.click(on_click_flag_button,
                                  inputs=[flags_dropdown, s_text_area, start_number],
                                  outputs=flags_dropdown)\
                           .then(lambda x: list(sorted(x, key=lambda y: int(y.split("🏷")[1]))),
                                 inputs=flags_dropdown,
                                 outputs=flags_dropdown)
                explain_button.click(lambda x: None,
                                     outputs=chatbot) \
                    .then(on_click_explain_button,
                          inputs=[text_area, start_number, end_number],
                          outputs=[chatbot, dialogue_area, prompt_area]) \
                    .then(after_response,
                          inputs=[s_text_area, dialogue_area],
                          outputs=suggest_area) \
                    .then(on_finish,
                          inputs=[s_text_area, dialogue_area])
                prompt_area.submit(on_submit_prompt_area,
                                   inputs=[s_text_area, dialogue_area, prompt_area],
                                   outputs=[chatbot, dialogue_area, prompt_area]) \
                    .then(lambda x: gr.update(visible=False),
                          outputs=suggest_area) \
                    .then(on_finish,
                          inputs=[s_text_area, dialogue_area])
interface.launch()
