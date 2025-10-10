# QR Item Tracking App

A web app for creating, storing, and retrieving item details. Each item generates a unique QR code that links directly to its detail page, making it easy to share and retrieve information.

## Dependencies

Backend: FastAPI (Python) for API endpoints

Database: SQLite with SQLAlchemy ORM

Frontend: HTML, CSS, JavaScript

QR Code Generation: qrcode (Python)

Version Control: Git & GitHub

# 🔧 Installation & Running Locally
## Clone repository
```
git clone https://github.com/Hider03/lock2.0.git
cd lock2.0

## Create python virtual environment
python -m venv .venv

## To activate venv on windows (its different for linux and mac)
.\.venv\Scripts\activate  

## Install dependencies
pip install -r requirements.txt

## Run backend in project main directory
uvicorn backend.main:app --reload
```

Then open http://127.0.0.1:8000 in your browser to run the api.
You can host the frontend however you want. (I used ngrok)

📂 Project Structure

```
LOCK2.0/
├── .db/
│ └── database.db
├── backend/
│ ├── pycache/
│ ├── init.py
│ ├── crud.py
│ ├── database.py
│ ├── email_utils.py
│ ├── main.py
│ ├── models.py
│ └── schemas.py
├── frontend/
│ ├── additem.html
│ ├── additem.js
│ ├── item.html
│ ├── landing.html
│ ├── landing.js
│ ├── lightmode.css
│ ├── loaditems.js
│ ├── login.html
│ ├── login.js
│ ├── profile.html
│ ├── profile.js
│ ├── pubitems.html
│ ├── register.html
│ ├── register.js
│ ├── script.js
│ ├── settings.html
│ ├── style.css
│ └── youritems.html
├── .env
├── .gitignore
├── .venv/
├── example.env
├── README.md
└── requirements.txt
```

## How It Works

User creates account. (The users information gets added to the SQLite Database file with the password being hashed using argon2)
User logs in with the created account. (An api call is made to check the users hashed password with the one used to log in and a JWT token is created)
User can add an item to their inventory of items with the following (The item gets added to the SQLite Database file)
  1. Item Description
  2. Direction if item is found
  3. Dropoff location
  4. Contact information (optional)
  
Once the item has been added, a QR Code gets generated.
That QR Code, once scanned, takes the "finder" to a public item page with the item info from earlier.
The "finder" can also send an email to the owner of the item using a company email to protect the owners identity.

## Screenshots / Demo

<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-additem-2025-10-10-19_53_14" src="https://github.com/user-attachments/assets/9e94834b-81ad-406c-930c-b34fbaf19431" />
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-youritems-2025-10-10-19_55_56" src="https://github.com/user-attachments/assets/bb2209f2-05d9-4beb-9284-76f577bc9f4b" />
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-pub-getitem-62565c47227486cd-2025-10-10-19_56_06" src="https://github.com/user-attachments/assets/6620a883-8027-45f1-b997-f36a24919da6" />
<img width="2050" height="2587" alt="screencapture-4857864d75f7-ngrok-free-app-2025-10-10-19_52_16" src="https://github.com/user-attachments/assets/e8cd1f0c-0877-4cf2-9803-46cc00438879" />
<img width="2050" height="1567" alt="screencapture-4857864d75f7-ngrok-free-app-register-2025-10-10-19_52_42" src="https://github.com/user-attachments/assets/fd4d1547-7200-47d0-868a-ec891b8dcd62" />
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-login-2025-10-10-19_52_54" src="https://github.com/user-attachments/assets/08c80e7b-11a1-4030-a4d5-6059f7fbf4ec" />


## 🌟 Future Improvements

Item categories & search

Allow users to change password and other details

Integrate Docker for broad usage without depending on environment

Deploy website on AWS
