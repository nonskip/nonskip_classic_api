import streamlit as st
import readpilot as rp
import re


def main():
    st.markdown(f"# 📚Readpilot - {rp.__version__}")
    text = st.text_area("Enter your paragraph here")
    # find the area in which the user has marked with (( )).
    if st.button("explain"):
        highlighted_text = re.findall(r'\(\((.*?)\)\)', text)[0]
        st.write(highlighted_text)
        # ask what highlighted text means in the context of the text
        d = rp.explain(text, highlighted_text)
        st.write(str(d))
        # retrieve vocabulary and log it to the dialogue
        d = rp.log(d)
        st.write(str(d))
        # get prompts
        # prompts = rp.suggest(d)
        # # ask the user to choose one of the prompts
        # prompt = st.selectbox("Choose one of the prompts", prompts)
        # # keep chatting
        # d = rp.chat(d, prompt)
        # st.write(str(d))
        # # for the time being, we end the chat here. get a string representation of the dialogue
        # st.write(str(d))


if __name__ == '__main__':
    main()


