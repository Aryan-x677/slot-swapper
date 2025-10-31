# 🗓️ Slot Swapper

## 🚀 Overview

**Slot Swapper** is a backend project built with **FastAPI**, designed to help users mark their time slots as `BUSY`, `SWAPPABLE`, or `SWAP_PENDING` and swap those slots with other users.  

The project supports **authentication, event management, and slot swapping logic** with proper validation and database relations.  

> 🧠 **Note:** This submission focuses mainly on the **backend development** part (as per the core challenge).  
> A minimal frontend is planned but not fully implemented — the backend API is complete, tested, and deployed.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy  
- **Database:** SQLite (can easily switch to PostgreSQL/MySQL)  
- **Auth:** JWT (OAuth2PasswordBearer)  
- **Deployment:** Render  
- **Containerization:** Docker  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Aryan-x677/slot-swapper.git
cd slot-swapper
```

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

### 3️⃣ Run Locally
```bash
uvicorn app.main:app --reload
```

Your app will run on 👉 `http://127.0.0.1:8000`

### 4️⃣ Run with Docker
```bash
# Build Docker image
docker build -t slot-swapper .

# Run container
docker run -d -p 8000:8000 slot-swapper
```

Then open `http://localhost:8000/docs` to test the API.

---

## 🌐 Deployment

The project is live at:  
🔗 **https://slot-swapper.onrender.com**

You can test all endpoints using Swagger UI at:  
👉 **https://slot-swapper.onrender.com/docs**

---

## 📚 API Endpoints

### 🔑 User Authentication

#### **POST** `/auth/signup`
Create a new user.

**Request**
```json
{
  "username": "aryan",
  "email": "aryan@example.com",
  "password": "12345"
}
```

**Response**
```json
{
  "message": "User created successfully"
}
```

---

#### **POST** `/auth/login`
Login and get JWT token.

**Request**
```x-www-form-urlencoded
username=aryan&password=12345
```

**Response**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

### 🗓️ Event Management

#### **POST** `/events/`
Create an event.

**Request**
```json
{
  "title": "Morning Meeting",
  "start_time": "2025-10-30T10:00:00",
  "end_time": "2025-10-30T12:00:00",
  "status": "SWAPPABLE"
}
```

**Response**
```json
{
  "id": 1,
  "title": "Morning Meeting",
  "status": "SWAPPABLE",
  "owner_id": 1
}
```

---

#### **GET** `/events/`
Fetch all events for the logged-in user.

**Response**
```json
[
  {
    "id": 1,
    "title": "Morning Meeting",
    "status": "SWAPPABLE"
  },
  {
    "id": 2,
    "title": "Gym Session",
    "status": "BUSY"
  }
]
```

---

### 🔁 Swap Logic

#### **GET** `/api/swappable-slots`
Fetch all `SWAPPABLE` slots from other users.

**Response**
```json
[
  {
    "id": 5,
    "title": "Team Meeting",
    "status": "SWAPPABLE",
    "owner_id": 2
  }
]
```

---

#### **POST** `/api/swap-request`
Send a swap request between two slots.

**Request**
```json
{
  "mySlotId": 2,
  "theirSlotId": 5
}
```

**Response**
```json
{
  "id": 1,
  "status": "PENDING",
  "requester_id": 1,
  "responder_id": 2
}
```

---

#### **POST** `/api/swap-response`
Accept or reject a swap request.

**Request**
```json
{
  "requestId": 1,
  "accept": true
}
```

**Response**
```json
{
  "id": 1,
  "status": "ACCEPTED"
}
```

---

## 🧩 Project Structure

```
slot_swapper_backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB connection setup
│   ├── routes/
│   │   ├── auth.py
│   │   ├── events.py
│   │   └── swap.py
│   └── utils/
│       └── passwd_handler.py
│
├── requirements.txt
├── Dockerfile
├── README.md
└── app.db
```

---

## 🧠 Notes

- ✅ All backend APIs are fully functional and tested on **Postman**.  
- 🧱 The **frontend part is not implemented**, as the focus was on backend logic, REST architecture, and API reliability.  
- 🐳 The app is Docker-ready for containerized deployment.  
- 🔐 JWT-based authentication and secure password hashing (PassLib) are implemented.

