import spacy
import textacy

def get_pps(doc):
    "Function to get PPs from a parsed document."
    pps = []
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        if token.pos_ == 'ADP':
            pp = ' '.join([tok.orth_ for tok in token.subtree])
            pps.append(pp)
    return pps

def get_subj(decomp):
    for token in decomp:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return str(decomp[start:end])

def get_obj(decomp):
    for token in decomp:
        if ("dobj" in token.dep_ or "pobr" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return str(decomp[start:end])

def detect_collocations(doc, parent_lemma, dep, child_lemma):
    """ Create a generator of all occurences of collocation in a document.
    The elements of generator are all pairs of tokens with lemmas `parent_lemma` and `child_lemma`
    and dependency of type `dep` between them that are found in a spacy document `doc`.
    """
    for token in doc:
        if token.lemma_ == parent_lemma:
            for child in token.children:
                if child.dep_ == dep and child.lemma_ == child_lemma:
                    yield token, child

def get_advcl(decomp):
    for token in decomp:
        # print(f"pos: {token.pos_}; lemma: {token.lemma_}; dep: {token.dep_}")
        if ("advcl" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return str(decomp[start:end])


def method_2(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    print("pps: ", get_pps(doc))
    print("subj: ", get_subj(doc))
    print("obj: ", get_obj(doc))
    print("advcl: ", get_advcl(doc))
    print("collocations: ", list(detect_collocations(doc, "break", "prt", "off")))

    patterns = [[{"POS" : "NOUN"}, {"POS" : "VERB"}], [{"POS" : "VERB"}, {"POS" : "ADP"}], [{"POS" : "VERB"}, {"POS" : "ADV"}], [{"POS" : "VERB"}], [{"POS" : "NOUN"}]]
    verb_phrases = textacy.extract.token_matches(doc, patterns = patterns)

    for verb_phrase in verb_phrases:
        print(verb_phrase)

    chunks = list(doc.noun_chunks)
    print(chunks)
    

    # for match_id, start, end
    return ""
#text = "The nuances of Paul’s greeting were not lost on the Reverend Mother."
text = "Hey guys break it off."
print(text+"\n")
method_2(text)

#https://stackoverflow.com/questions/64823090/how-to-search-for-separable-phrases-in-text
#아니면 직접 register
# matcher.add("called off", [pattern])

# doc = nlp("There won't be any calling them off.")

# result = matcher(doc)

# positions = {t for pattern, pair in result for t in pair}
# for token in doc:
#     print('_{}_'.format(token) if token.i in positions else token, end=' ')