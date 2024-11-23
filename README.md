# Military Intelligence Data Collection and Analysis Platform

## Overview
A real-time military intelligence platform developed for the [Defense Tech Hackathon](https://www.defense-tech-hackathon.com/). This system provides advanced data collection, analysis, and visualization capabilities for military intelligence operations.

## Key Features
- Real-time intelligence data collection and processing
- Interactive map visualization with threat indicators
- Multi-language support (English, Ukrainian, Russian)
- Alert system with priority levels
- Credibility scoring system
- Timeline view of intelligence events
- Secure authentication system

## Tech Stack
- Backend: Flask, SQLAlchemy, Socket.IO
- Frontend: Bootstrap, Leaflet.js
- Database: PostgreSQL
- NLP: SpaCy, Transformers
- Real-time: WebSocket

## Security Features
- Secure authentication system
- CSRF protection
- Session management
- Input validation
- SQL injection prevention

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `DATABASE_URL`: PostgreSQL database URL
   - `FLASK_SECRET_KEY`: Secret key for Flask session
   - `OPENWEATHERMAP_API_KEY`: API key for location data (optional)
4. Initialize the database:
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ```
5. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Access the platform through the web interface
2. Log in using provided credentials:
   - Default admin credentials:
     - Username: admin
     - Password: admin123 (change upon first login)
3. Monitor the dashboard for real-time updates
4. Review and manage alerts
5. Generate intelligence reports

## Contributing
This project was developed for the Defense Tech Hackathon. For contributions or issues, please contact the development team.

## License
Proprietary - All rights reserved
