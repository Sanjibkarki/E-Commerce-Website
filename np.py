import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is my passion, Music is goat.")
for token in doc.ents:
    print(token)
