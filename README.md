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
project/
├── backend/
│   ├── main.py          # FastAPI backend
│   ├── models.py        # SQLAlchemy models
│   └── items.db         # SQLite database
├── static/
│   ├── style.css        # Frontend styling
│   └── script.js        # Frontend logic
├── templates/
│   └── index.html       # Item creation & QR display
└── README.md
```

## How It Works

User fills out the form with item details.
Backend saves the item into SQLite database.
A unique item ID is generated.
A QR code is displayed linking to /items/{id}.
Clicking or scanning the QR code loads the item detail page.

## Screenshots / Demo


# 🔧 Installation & Running Locally
## Clone repository
```
git clone https://github.com/yourusername/qr-item-app.git
cd qr-item-app

## Install dependencies
pip install -r requirements.txt

## Run backend
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

## 🌟 Future Improvements

User authentication

Item categories & search

Cloud database integration (PostgreSQL)

Deployment on Heroku/Render
