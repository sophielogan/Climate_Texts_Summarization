import spacy
import pandas as pd 
import numpy as np

spacy.cli.download("en_core_web_sm")
NER = spacy.load("en_core_web_sm")

def spacy_large_ner(document):
  return {(ent.text.strip(), ent.label_) for ent in NER(document).ents}
