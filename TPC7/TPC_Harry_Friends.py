import spacy
from spacy.matcher import Matcher

# 1. Setup
file = open("Harry Potter e A Pedra Filosofal.txt", "r", encoding="utf-8")
text = file.read()
file.close()

nlp = spacy.load("pt_core_news_lg")
matcher = Matcher(nlp.vocab)

pattern = [
    {"ENT_TYPE": "PER", "OP": "+"},
    {"TEXT": {"NOT_IN": [".", "!", "?"]}, "OP": "*"},  #"NOT_IN" garante que o match não "salte" de uma frase para a outra
    {"ENT_TYPE": "PER", "OP": "+"}
]
matcher.add("AMIZADE_ESTRITA", [pattern])

doc = nlp(text)
amizades = {}

for sent in doc.sents:
    matches = matcher(sent)
    
    for match_id, start, end in matches:
        span = sent[start:end]
        
        # Dicionário para nomes únicos neste match específico
        nomes_no_match = {}
        for ent in span.ents:
            if ent.label_ == "PER":
                n = ent.text.strip().replace(".", "")
                if len(n) > 2:
                    nomes_no_match[n] = True #Para grantir que o mesmo nome quando aparece mais que uma vez na frase, não seja contado.
        
        # Guardar no dicionário principal
        if len(nomes_no_match) > 1:
            for p1 in nomes_no_match:
                if p1 not in amizades:
                    amizades[p1] = {}
                for p2 in nomes_no_match:
                    if p1 != p2:
                        if p2 in amizades[p1]:
                            amizades[p1][p2] += 1
                        else:
                            amizades[p1][p2] = 1

import json
print(json.dumps(amizades, indent=4, ensure_ascii=False))