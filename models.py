from datetime import datetime
import enum
from sqlalchemy.types import JSON
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db
class MediaType(enum.Enum):
    text = 'text'
    image = 'image'
    video = 'video'
    audio = 'audio'

class IntelType(enum.Enum):
    IMINT = 'IMINT'
    SIGINT = 'SIGINT'
    HUMINT = 'HUMINT'
    OSINT = 'OSINT'
    CYBERINT = 'CYBERINT'

class SourceReliability(enum.Enum):
    A = 'A'  # Completely reliable
    B = 'B'  # Usually reliable
    C = 'C'  # Fairly reliable
    D = 'D'  # Not usually reliable
    E = 'E'  # Unreliable
    F = 'F'  # Reliability cannot be judged

class InfoCredibility(enum.Enum):
    ONE = '1'    # Confirmed by other sources
    TWO = '2'    # Probably true
    THREE = '3'  # Possibly true
    FOUR = '4'   # Doubtful
    FIVE = '5'   # Improbable
    SIX = '6'    # Truth cannot be judged

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='analyst')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class IntelligenceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    credibility_score = db.Column(db.Float)
    language = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    verified = db.Column(db.Boolean, default=False)
    media_type = db.Column(db.Enum(MediaType), default=MediaType.text)
    media_url = db.Column(db.String(500))
    media_metadata = db.Column(JSON)
    # New fields for intelligence classification
    intel_type = db.Column(db.Enum(IntelType), nullable=False, default=IntelType.OSINT)
    intel_subtype = db.Column(db.String(50))
    source_reliability = db.Column(db.Enum(SourceReliability), nullable=False, default=SourceReliability.F)
    info_credibility = db.Column(db.Enum(InfoCredibility), nullable=False, default=InfoCredibility.SIX)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    priority = db.Column(db.Integer)  # 1-5, 1 being highest
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))  # new, acknowledged, resolved
    intel_id = db.Column(db.Integer, db.ForeignKey('intelligence_data.id'))
<<<<<<< HEAD

class ConversationAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority_level = db.Column(db.String(50), nullable=False)  # High, Medium, Low
    risk_assessment = db.Column(db.Text, nullable=False)
    key_insights = db.Column(db.Text, nullable=False)
    critical_entities = db.Column(JSON, nullable=False)
    locations_mentioned = db.Column(JSON, nullable=False)
    sentiment_summary = db.Column(db.Text, nullable=False)
    source_reliability = db.Column(db.String(50), nullable=False)
    information_credibility = db.Column(db.String(50), nullable=False)
    recommended_actions = db.Column(JSON, nullable=False)
    entity_relationships = db.Column(db.Text, nullable=False)
    speakers = db.Column(JSON, nullable=False)
    conversation_duration = db.Column(db.String(50), nullable=False)  # Short, Medium, Long
    analyzed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
=======
>>>>>>> 31a7b0d (Restored to 'f2f54e23bd383fb654e2f126b94e246f90034721')
