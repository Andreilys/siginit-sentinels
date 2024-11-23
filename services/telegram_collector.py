import asyncio
from telethon import TelegramClient
from app import db
from models import IntelligenceData
from services.nlp_processor import process_text
from geopy.geocoders import Nominatim

class TelegramCollector:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient('intel_bot', api_id, api_hash)
        self.geolocator = Nominatim(user_agent="intel_platform")
        
    async def start_collection(self, channel_urls):
        await self.client.start()
        
        @self.client.on(events.NewMessage(chats=channel_urls))
        async def handle_new_message(event):
            message = event.message.text
            
            # Process text through NLP
            processed_data = process_text(message)
            
            # Extract location if available
            location = None
            if processed_data['location']:
                try:
                    location = self.geolocator.geocode(processed_data['location'])
                except:
                    pass
                
            intel_data = IntelligenceData(
                source=event.chat.title,
                content=message,
                credibility_score=self.calculate_credibility(event),
                language=processed_data['language'],
                latitude=location.latitude if location else None,
                longitude=location.longitude if location else None
            )
            
            db.session.add(intel_data)
            db.session.commit()
            
    def calculate_credibility(self, event):
        # Basic credibility scoring based on channel metrics
        score = 0.5  # Base score
        if hasattr(event.chat, 'participants_count'):
            if event.chat.participants_count > 10000:
                score += 0.2
        return min(score, 1.0)
