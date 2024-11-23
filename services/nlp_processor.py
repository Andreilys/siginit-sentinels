from transformers import pipeline
import spacy
from langdetect import detect

class NLPProcessor:
    def __init__(self):
        self.models_available = False
        try:
            import spacy
            self.nlp_en = spacy.load('en_core_web_sm')
            try:
                self.nlp_ru = spacy.load('ru_core_news_sm')
            except OSError:
                self.nlp_ru = None
                print("Russian language model not available, will use English model for all text")
            self.models_available = True
        except Exception as e:
            print(f"NLP models not available: {str(e)}")
            self.nlp_en = None
            self.nlp_ru = None
        
    def process_text(self, text):
        try:
            language = detect(text)
        except:
            language = 'en'
        
        entities = []
        if self.models_available and self.nlp_en and self.nlp_ru:
            try:
                nlp = self.nlp_ru if (language == 'ru' and self.nlp_ru) else self.nlp_en
                doc = nlp(text)
                entities = self.extract_entities(doc)
            except Exception as e:
                print(f"Error processing text: {str(e)}")
                # Return empty entities on error
            
        return {
            'language': language,
            'entities': entities,
            'location': self.extract_location(entities),
            'military_entities': self.extract_military_entities(text)
        }
        
    def extract_entities(self, doc):
        if not self.models_available:
            return []
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
