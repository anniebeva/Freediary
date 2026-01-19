# Freediary

Freediary is a personal project built with Flask, inspired by my interest in freediving. 
It is designed as a personal tool for tracking trainings and exercises, and also serves as practice for building web applications with Flask.

---

## Features

Currently, Freediary allows you to:

- Add and edit trainings of different types: **Pool**, **Gym**, **Depth**
- Add exercises associated with each training
- Filter trainings by type
- Track training details like difficulty, notes, and type-specific fields
- Simple UI with Bootstrap for responsive and clean design
- Draft system for exercises before saving a training
- Uses SQLite as database

---

## Installation & Setup

1. **Clone the repository**

git clone https://github.com/yourusername/freediary.git
cd freediary

2. **Create a virtual environment**

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

3. **Install dependencies**

pip install -r requirements.txt


4. **Initialize the database**

from app import db
db.create_all()

5. **Run the Flask app**

export FLASK_APP=run.py
export FLASK_ENV=development
flask run

6. Your app should now be running at http://127.0.0.1:5000

## Project Structure

## Future Plans and ideas

Freediary is still a work-in-progress. Planned improvements include:

*User authentication: adding login, account, user-specific trainings*

*Better structure and scalability: Refactor routes, directories, database tables*

*Add tests using Pytest*

*Telegram bot integration*

*More training options and exercises: Extend pool, gym, and depth exercises*

*Analytics & stats: Track performance and progress, statistics page*

*Better UI and design*

*Custom training types & exercises: Users can add their own*

*Training calendar and plan, reminders*

## Notes
This project was created primarily as a personal tool and Flask practice.

All current functionality is geared toward personal use.

The UI is responsive but simple; Bootstrap is used for styling.

No authentication yet, so all data is accessible without login.

