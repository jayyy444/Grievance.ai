GrievanceAI
Smart Municipal Complaint Management System
Python  Flask  SQLite  NLP  Railway  

Overview
GrievanceAI is an AI-powered civic complaint management platform designed to streamline the process of filing and resolving municipal grievances. Built with Flask and NLP, it automatically categorizes complaints, detects urgency using sentiment analysis, and provides a real-time admin dashboard for municipal officers.
The project was built to solve a real problem — citizens of cities like Dhule, Maharashtra face no structured, transparent channel to file civic complaints. GrievanceAI provides exactly that.

Key Features
•	AI Complaint Categorization — NLP keyword engine classifies complaints into 10+ categories (Sanitation, Infrastructure, Water Supply, Electricity, Public Safety, etc.)
•	Sentiment Analysis — TextBlob-powered urgency detection (Low / Medium / High / Critical) based on complaint language
•	Interactive AI Chatbot — 6-step guided chatbot for complaint submission, no form-filling needed
•	Admin Dashboard — Real-time overview with category/urgency charts, complaint management, and status updates
•	User Authentication — Secure registration and login with Flask-Login and Werkzeug password hashing
•	Complaint Status Tracking — Citizens can track their complaint status with a visual timeline
•	Role-Based Access — Separate portals for citizens and admin officers
•	Railway Deployment Ready — Gunicorn + Procfile, no extra configuration needed

Tech Stack
Backend
Framework:  Flask 3.0.3
Database ORM:  Flask-SQLAlchemy 3.1.1 + SQLAlchemy 2.0
Authentication:  Flask-Login 0.6.3 + Werkzeug 3.0.3
NLP / AI:  TextBlob 0.18.0 + Custom keyword classifier
Server:  Gunicorn 22.0.0
Language:  Python 3.11
Frontend
Markup:  Jinja2 HTML Templates
Styling:  Custom CSS (Sora + DM Sans fonts, CSS variables)
Interactivity:  Vanilla JavaScript (Fetch API for chatbot)
Database
Development:  SQLite (auto-created on first run)
Production:  PostgreSQL (Railway managed, psycopg2-binary)
Deployment
Platform:  Railway (Free Tier)
Config:  Environment variables (SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD)

Project Structure
grievance-ai/ ├── app.py               # App factory, DB init, admin seeding ├── config.py            # Railway + local config, env vars ├── models.py            # User and Complaint SQLAlchemy models ├── ai_utils.py          # NLP categorization + sentiment analysis ├── routes/ │   ├── auth.py          # Register, login, logout │   ├── complaints.py    # Submit, list, track, chatbot API │   └── admin.py         # Admin dashboard, manage complaints ├── chatbot/ │   └── chatbot.py       # 6-step guided chatbot logic ├── static/ │   ├── style.css        # Full custom UI design system │   └── script.js        # Chatbot frontend + interactions ├── templates/           # 9 Jinja2 HTML templates │   └── admin/           # 3 admin-specific templates ├── requirements.txt     # All pinned dependencies ├── Procfile             # gunicorn command for Railway ├── runtime.txt          # Python 3.11.9 └── .gitignore           # venv, __pycache__, *.db excluded

Installation & Local Setup
Prerequisites
•	Python 3.9 or above
•	pip (Python package installer)
•	Git
Steps
1.	Clone the repository
git clone https://github.com/YOUR_USERNAME/GrievanceAI.git && cd GrievanceAI
2.	Create virtual environment
python -m venv venv && venv\Scripts\activate   # Windows source venv/bin/activate                       # Mac/Linux
3.	Install dependencies
pip install -r requirements.txt
4.	Run the application
python app.py
Open http://localhost:5000 in your browser.
Default admin credentials — Email: admin@grievanceai.com | Password: Admin@1234

Deploying to Railway
5.	Push your code to a GitHub repository (ensure .gitignore is committed)
6.	Go to railway.app → New Project → Deploy from GitHub Repo
7.	Railway auto-detects the Procfile and deploys automatically
8.	Set environment variables in the Variables tab:
•	SECRET_KEY — any long random string
•	ADMIN_EMAIL — your admin email
•	ADMIN_PASSWORD — secure admin password

AI & NLP Components
Complaint Categorization
A custom keyword-matching NLP engine scans the complaint title and description for domain-specific terms across 10 categories. Each word match contributes to a category score, and the highest-scoring category is assigned. No training data required — works reliably out of the box.
Sentiment-Based Urgency Detection
The system first checks for urgency keywords (emergency, critical, dangerous, etc.) for deterministic high-stakes detection. If no keyword match, TextBlob's polarity score determines urgency on a -1.0 to +1.0 scale. Polarity below -0.5 maps to High urgency; -0.1 to -0.5 maps to Medium; above -0.1 maps to Low.
AI Chatbot
A 6-step rule-based conversational chatbot guides users through the complaint submission flow. At the end, the AI analysis runs automatically and the complaint is submitted — no form needed. Supports option buttons for quick selection and free-text input.

API Endpoints
GET  /  Landing page
GET  /register  Registration form
POST /register  Create new user account
GET  /login  Login form
POST /login  Authenticate user
GET  /logout  Log out and clear session
GET  /dashboard  User dashboard (auth required)
GET  /submit  Complaint submission form
POST /submit  Submit complaint with AI analysis
GET  /my-complaints  List all user complaints (paginated, filterable)
GET  /track/<id>  Complaint status tracker with timeline
GET  /chatbot  AI chatbot interface
POST /api/chat  Chatbot message API (JSON)
GET  /admin/  Admin dashboard with stats and charts
GET  /admin/complaints  All complaints with filters
GET/POST /admin/complaint/<id>  View and update complaint status

Contributing
Contributions are welcome. Please fork the repository, create a feature branch, make your changes, and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

Contact
Developer:  JAYKUMAR
Institution:  SVKM Institute of Technology, Dhule, Maharashtra
University:  Dr. Babasaheb Ambedkar Technological University (DBATU)
Email:  jayc31665@gmail.com
GitHub:  github.com/jayyy444
