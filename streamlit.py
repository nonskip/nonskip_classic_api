import streamlit as st
import readpilot as rp
import re


@st.cache_data
def explain(text: str, h_text: str) -> rp.Dialogue:
    st.session_state['explain_pressed'] = True
    d = rp.explain(text, h_text)
    return d


@st.cache_data
def suggest(_d: rp.Dialogue) -> list[str]:
    st.session_state['suggest_pressed'] = True
    prompts = rp.suggest(_d)
    return prompts


def main():
    st.markdown(f"# 📚Readpilot - {rp.__version__}")
    # set the height of the area to be reasonably spacy
    text = st.text_area("Enter your paragraph here", height=1000)
    # find the area in which the user has marked with (( )).
    if st.session_state.get('explain_pressed', False) or st.button("explain"):
        h_text = re.findall(r'\(\((.*?)\)\)', text)[0]
        st.write(h_text)
        # ask what highlighted text means in the context of the text
        d = explain(text, h_text)
        st.write(d.messages[-1].content)
        # get suggested prompts
        prompts = suggest(d)
        # ask the user to choose one of the prompts
        prompt = st.selectbox("Choose a follow-up question to ask", prompts)
        if st.session_state.get('ask_pressed', False) or st.button("ask"):
            # keep chatting
            with st.spinner("asking..."):
                d = rp.chat(prompt, d)
                st.write(d.messages[-1].content)


if __name__ == '__main__':
    main()


