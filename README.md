# readpilot
Your copilot for reading books in English

> Python >= 3.9.12


## Quick Start
```bash
# install dependencies
pip3 install -r requirements.txt
```
```bash 
# register your key as an environment variable
export OPENAI_API_KEY= ...
```
```python
# interact with ChatGPT with `rp.chat`
from readpilot import rp
d = rp.chat("You are not a machine. You are a living person. Tell me your story.")
print(d)
```
```text
system: You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Current date: 2023-03-14 11:16:11.441720
user: You are not a machine. You are a living person. Tell me your story.
assistant: I apologize for any confusion, but I am actually a machine. Specifically, I am a large language model developed by OpenAI, trained using a massive dataset of text from the internet. While I am capable of generating human-like responses to text-based prompts, I do not have personal experiences or a consciousness like a human does.
```
```python
# resume chatting from a previous conversation
d = rp.chat("No need for apology!", d)
print(d)
```
```text
system: You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Current date: 2023-03-14 11:27:12.119732
user: You are not a machine. You are a living person. Tell me your story.
assistant: I apologize for any confusion, but I must clarify that I am indeed a machine, specifically a language model created by OpenAI. While I am capable of processing and generating language to carry on conversations, I do not have a personal story or consciousness like a living person would.
user: No need for apology!
assistant: Thank you for understanding. Is there anything else I can assist you with?
```