from transformers import pipeline
import spacy
from langdetect import detect

class NLPProcessor:
    def __init__(self):
        self.nlp_en = spacy.load('en_core_web_sm')
        self.nlp_ru = spacy.load('ru_core_news_sm')
        self.ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        
    def process_text(self, text):
        language = detect(text)
        
        if language == 'ru':
            doc = self.nlp_ru(text)
        else:
            doc = self.nlp_en(text)
            
        entities = self.extract_entities(doc)
        location = self.extract_location(entities)
        
        return {
            'language': language,
            'entities': entities,
            'location': location,
            'military_entities': self.extract_military_entities(text)
        }
        
    def extract_entities(self, doc):
        return [(ent.text, ent.label_) for ent in doc.ents]
        
    def extract_location(self, entities):
        for entity, label in entities:
            if label in ['LOC', 'GPE']:
                return entity
        return None
        
    def extract_military_entities(self, text):
        # Custom military entity extraction
        military_terms = ['tank', 'artillery', 'troops', 'battalion']
        return [term for term in military_terms if term.lower() in text.lower()]
