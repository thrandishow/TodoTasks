# 📝 ✅ TodoTasks 🌿

**TodoTasks** is a modern, lightweight, and asynchronous task management API built with 🌱 **FastAPI**. It features **JWT-based authentication** 🔐, an **async database** for smooth performance ⚡, and is designed to help you manage your to-dos with simplicity and speed.  

[![Python Version](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)  
[![Build Status](https://img.shields.io/badge/Build-v0.1.0-green)](https://github.com/yourusername/TodoTasks/actions)  
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

✅ **JWT Authentication**  
Secure API endpoints using JSON Web Tokens (JWT).  

✅ **Asynchronous Database**  
Leveraging async ORM for high performance and scalability.  

✅ **FastAPI Framework**  
Enjoy the blazing speed and intuitive design of FastAPI.  

✅ **CRUD for Tasks**  
Create, Read, Update, Delete your tasks effortlessly.  

✅ **Modern API Design**  
OpenAPI/Swagger docs auto-generated for easy testing.  

✅ **Poetry**
Poetry used for dependencies. 🌱
---

## 🖥️ Screenshots

| 🗂️ Task List View | 🔐 Authentication |
|--------------------|---------------------|
| ![Task List](https://your-image-link-here.com/tasks.png) | ![Auth](https://your-image-link-here.com/auth.png) |

---

## 🚀 Tech Stack

🌿 **Backend:** [FastAPI](https://fastapi.tiangolo.com/)  
🔋 **Authentication:** JWT Tokens  
⚡ **Database:** Async DB (e.g., SQLAlchemy + Databases or Tortoise ORM)  
📄 **Documentation:** Auto-generated Swagger UI  

---

## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/thrandishow/TodoTasks.git
   cd TodoTasks
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install poetry
   poetry install --no-root
   ```

4. **Set environment variables** (update `.env` with your secret keys)

5. **Run the server**
   ```bash
   uvicorn src.main:app --reload
   ```

---

## 📖 API Documentation

Interactive API docs available at:  

🔗 [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)  
🔗 [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc)  

---

## 📂 Project Structure

```
TodoTasks/
│
├── src/
│   ├── models/          # Models folder
│   ├── schemas/         # Pydantic schemas folder
│   ├── auth.py/         # JWT authentication utils
│   ├── core/            # Settings folder
|   ├── migrations/      # Async alembic
│   ├── routers/         # Routers folder
│   ├── repositories/    # Pattern reposytory
│   ├── auth/            # Auth settings
│   ├── database.py      # Async DB setup
|   └── main.py          # FastAPI application
│
├── pyproject.toml       # Project dependencies
├── .env                 # Environment variables
└── README.md            # Project description
```

---

## 🛡️ Security

- Passwords are hashed using **bcrypt** 🔐.
- Tokens are time-limited and refreshable.

---

## ✨ Contribution

Contributions are welcome! 🌿 Please fork the repo and submit a pull request.  

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🌱 Stay Green & Async ⚡

> _“A productive day starts with a clean todo list!”_

---
