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
git clone https://github.com/Hider03/QRKey.git
cd QRKey

## Create python virtual environment
python -m venv .venv

## To activate venv on windows (its different for linux and mac)
.\.venv\Scripts\activate  

## Install dependencies
pip install -r requirements.txt

## At this point you should fill out your own .env file using the example.env provided

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

- User creates account. (The users information gets added to the SQLite Database file with the password being hashed using argon2)
- User logs in with the created account. (An api call is made to check the users hashed password with the one used to log in and a JWT token is created)
- User can add an item to their inventory of items with the following (The item gets added to the SQLite Database file)
  1. Item Description
  2. Direction if item is found
  3. Dropoff location
  4. Contact information (optional)
  
- Once the item has been added, a QR Code gets generated.
- That QR Code, once scanned, takes the "finder" to a public item page with the item info from earlier.
- The "finder" can also send an email to the owner of the item using a company email to protect the owners identity.

## Screenshots / Demo

Landing Page
<img width="2050" height="2587" alt="screencapture-4857864d75f7-ngrok-free-app-2025-10-10-19_52_16" src="https://github.com/user-attachments/assets/a20ae1fe-cae1-4a4f-a5d2-cc9e941a4a2c" />
Register page
<img width="2050" height="1567" alt="screencapture-4857864d75f7-ngrok-free-app-register-2025-10-10-19_52_42" src="https://github.com/user-attachments/assets/915d9efa-e177-48a3-a33a-484d65c2109d" />
Login Page
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-login-2025-10-10-19_52_54" src="https://github.com/user-attachments/assets/184c2c37-7fa8-4a32-a006-fd29a21a81b7" />
Profile page
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-profile-2025-10-10-19_59_10" src="https://github.com/user-attachments/assets/903a8152-ff10-48e6-8ca4-d21d437fc8d3" />
Item Creation page
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-additem-2025-10-10-19_53_14" src="https://github.com/user-attachments/assets/fa06d7f4-5385-452d-b3de-d95fe094d81b" />
Item page (Only visable to a logged in user)
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-youritems-2025-10-10-20_01_38" src="https://github.com/user-attachments/assets/d2413050-c87e-45c5-8efc-686c80e8a63a" />
Public Item page (When QR code is scanned)
<img width="2050" height="1324" alt="screencapture-4857864d75f7-ngrok-free-app-pub-getitem-62565c47227486cd-2025-10-10-20_01_46 (1)" src="https://github.com/user-attachments/assets/19732282-2c6e-4ded-9dcd-409b6efffb46" />

## 🌟 Future Improvements

Item categories & search

Allow users to change password and other details

Integrate Docker for broad usage without depending on environment

Deploy website on AWS
