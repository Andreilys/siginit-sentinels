from app import db, socketio
from models import Alert, IntelligenceData
from datetime import datetime

class AlertManager:
    def __init__(self):
        self.threshold_configs = {
            'troop_movement': 0.7,
            'equipment_concentration': 0.8,
            'civilian_threat': 0.6
        }
        
    def process_intel(self, intel_data):
        threat_level = self.calculate_threat_level(intel_data)
        
        if threat_level > 0.8:
            self.create_alert(intel_data, priority=1)
        elif threat_level > 0.6:
            self.create_alert(intel_data, priority=2)
        elif threat_level > 0.4:
            self.create_alert(intel_data, priority=3)
            
    def calculate_threat_level(self, intel_data):
        # Implement threat level calculation logic
        base_threat = 0.5
        
        if intel_data.credibility_score > 0.8:
            base_threat += 0.2
            
        # Add more threat calculation logic
        
        return min(base_threat, 1.0)
        
    def create_alert(self, intel_data, priority):
        alert = Alert(
            title=f"Priority {priority} Alert",
            description=intel_data.content[:200],
            priority=priority,
            status='new',
            intel_id=intel_data.id
        )
        
        db.session.add(alert)
        db.session.commit()
        
        # Emit WebSocket event
        socketio.emit('new_alert', {
            'id': alert.id,
            'priority': priority,
            'title': alert.title
        })
