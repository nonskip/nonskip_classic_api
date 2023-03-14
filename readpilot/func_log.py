import os

import openai
from dotenv import load_dotenv

from . import Dialogue

load_dotenv()

openai.api_key = os.getenv('API_KEY')

engine = "gpt-3.5-turbo"

def get_vocab(h_text: str) -> list:
    # get the vocabulary from the highlighted text
    # param h_text: the highlighted text to find vocabulary from.
    # return: a list of vocabulary.
    
        # split the highlighted text into words
        words = h_text.split(' ')
    
        # remove punctuation
        vocab = []
        for word in words:
            # remove punctuation
            word = word.strip('.,?!;:')
    
            # remove empty strings
            if word != '':
                vocab.append(word)
    
        return vocab

def log(d: Dialogue, h_text: str) -> Dialogue:
    # log the dialogue to a database. For the time being, we will use a local database.
    # param d: a Dialogue object.
    # param h_text: the highlighted text to find vocabulary from.
    # return: a Dialogue object with the new vocabulary added.

    # get the vocabulary from the highlighted text
    vocab = get_vocab(h_text)

    # add the vocabulary to the dialogue
    d.vocab.extend(vocab)

    return d


