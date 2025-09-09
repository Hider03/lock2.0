# QR Item Tracking App

A web app for creating, storing, and retrieving item details. Each item generates a unique QR code that links directly to its detail page, making it easy to share and retrieve information.

## Features

Add items with description, directions, drop-off location, and contact info.

Generate a QR code that links directly to the item’s details page.

Retrieve item information via dynamic routes (/items/{id}).

Clean, responsive UI.

## Skills & Technologies Used

Backend: FastAPI (Python) for API endpoints

Database: SQLite with SQLAlchemy ORM

Frontend: HTML, CSS, JavaScript

QR Code Generation: qrcode JavaScript library

Asynchronous Requests: fetch() API for POST/GET

Deployment-ready Structure: Static file serving, database migrations

Version Control: Git & GitHub

📂 Project Structure

```
LOCK2.0/
├── .db/
│   └── items.db
├── backend/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── schemas.py
├── frontend/
│   ├── fonts/
│   ├── index.html
│   ├── item.html
│   ├── script.js
│   └── style.css
└── .gitignore
```

## How It Works

User fills out the form with item details.
Backend saves the item into SQLite database.
A unique item ID is generated.
A QR code is displayed linking to /items/{id}.
Clicking or scanning the QR code loads the item detail page.

## Screenshots / Demo
<img width="1421" height="1398" alt="Screenshot 2025-09-09 041551" src="https://github.com/user-attachments/assets/5f366ebb-a80b-4191-8ad0-5d57741708ed" />
<img width="1418" height="1445" alt="Screenshot 2025-09-09 041642" src="https://github.com/user-attachments/assets/fa9c3681-ac41-4f35-837c-9d13c90c403c" />
<img width="1433" height="1322" alt="Screenshot 2025-09-09 041656" src="https://github.com/user-attachments/assets/8d4e0a53-2dec-4da1-81b7-3374388a2856" />


# 🔧 Installation & Running Locally
## Clone repository
```
git clone https://github.com/yourusername/lock2.0.git
cd lock2.0

## Install dependencies
pip install -r requirements.txt

## Run backend in project main directory
uvicorn backend.main:app --reload
```

Then open http://127.0.0.1:8000 in your browser to run the api.
You can host the frontend however you want. (I used ngrok)

## 🌟 Future Improvements

User authentication

Item categories & search

Cloud database integration (PostgreSQL)

Deployment on Heroku/Render
