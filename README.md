# 🚀 Task Management API

Backend Developer Intern Assignment – RESTful API with Authentication & Database Integration

---

## 📌 Overview

This project is a **secure, RESTful Task Management API** that allows users to register, authenticate, and manage their tasks.

It demonstrates:

* Authentication using JWT
* Integration with **PostgreSQL (users)** and **MongoDB (tasks)**
* Role-based access control (user-specific tasks)
* Data validation and structured error handling

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Python)
* **Authentication:** JWT (JSON Web Tokens)
* **Database:**

  * PostgreSQL → User data
  * MongoDB → Task data
* **ORM/ODM:**

  * SQLAlchemy (PostgreSQL)
  * Motor / PyMongo (MongoDB)
* **Validation:** Pydantic
* **Password Hashing:** argon
* **Environment Management:** python-dotenv

---

## 📂 Project Structure

```
project/
│── database/
│   ├── database_sql.py
│   ├── database_mongo.py
│
│── models.py
│
│── schemas/
│   ├── user_schema.py
│   ├── task_schema.py
│
│── routers/
│   ├── auth.py
│   ├── delete_account.py
    ├── task_manage.py
│
│── utils/
    ├── config.py
│   ├── dependencies.py
│   ├── security.py
│
│── main.py
│── .env
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd project
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost/dbname
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 5️⃣ Run Application

```bash
uvicorn main:app --reload
```

---

### 6️⃣ Open API Docs

👉 http://127.0.0.1:8000/docs

---

## 🔐 Authentication

* Uses **JWT Token**
* Pass token in header:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### 🧑 User Management

#### ➤ Register User

`POST /auth/register`

**Request:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

---

#### ➤ Login

`POST /auth/login`

**Response:**

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```


---

## 📋 Task Management

### ➤ Create Task

`POST /user/tasks`

```json
{
  "title": "Complete API",
  "description": "Finish backend",
  "status" : "pending",
  "due_date": "2026-04-20T10:00:00",
  "priority": "high"
}
```

---

### ➤ Get All Tasks

`GET /user/tasks`

---

### ➤ Get Single Task

`GET /user/tasks/{task_id}`

---

### ➤ Update Task (Partial)

`PATCH /user/tasks/{task_id}`

```json
{
  "status": "completed"
}
```

---

### ➤ Delete Task

`DELETE /user/tasks/{task_id}`

---

## 🔒 Security Features

* Password hashing using bcrypt
* JWT-based authentication
* User-specific data isolation
* Protected routes using dependencies

---

## ⚠️ Error Handling

Standard HTTP responses:

| Code | Meaning               |
| ---- | --------------------- |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 404  | Not Found             |
| 422  | Validation Error      |
| 500  | Internal Server Error |

---

## ✅ Validation

* Email format validation
* Required fields enforcement
* Enum validation (status, priority)
* Custom validators (no blank strings)

---

## 🎯 Key Design Decisions

* **Separate DBs:**
  PostgreSQL for structured user data
  MongoDB for flexible task schema

* **Layered architecture:**
  Routers → Schemas → Models → Database

* **PATCH support:**
  Partial updates using `exclude_unset=True`

---

## 🧪 Testing

You can test endpoints via:

* Swagger UI (`/docs`)
* Postman

---

## 📹 Demo Requirements

Demonstrated:

* User registration & login
* JWT authentication
* Task CRUD operations
* Unauthorized access prevention
* Validation & error handling

---

## 🚀 Future Improvements

* Role-based access control
* Pagination for tasks
* Docker setup
* Unit testing
* Rate limiting

---


Backend Developer (Python | FastAPI | MongoDB | PostgreSQL)

---
