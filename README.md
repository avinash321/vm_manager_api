# 🚀 VM Manager API

A scalable and production-ready **Virtual Machine Management API** built using **FastAPI**, **PostgreSQL**, and **JWT Authentication**.

This project demonstrates a clean backend architecture with modular design, authentication, and VM lifecycle management.

---

## 📌 Features

* 🔐 User Authentication (JWT-based login/register)
* 🔑 Secure password hashing using Argon2
* 🖥️ VM Management (CRUD operations)
* 🗄️ PostgreSQL database integration
* 📦 Modular FastAPI project structure
* 📜 Centralized logging (info, warning, error)
* 🚀 Production-ready design (scalable & maintainable)

---

## 🏗️ Project Structure

```
vm_manager/
│
├── app/
│   ├── main.py                # Entry point
│   │
│   ├── core/                 # Config & logging
│   │   ├── config.py
│   │   └── logger.py
│   │
│   ├── db/                   # Database setup
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── schemas/              # Pydantic schemas
│   │   └── schemas.py
│   │
│   ├── api/                  # API routes
│   │   ├── auth.py
│   │   ├── vm.py
│   │   └── deps.py
│   │
│   ├── services/             # Business logic
│   │   ├── auth_service.py
│   │   └── vm_service.py
│   │
│   └── utils/                # Utilities
│       └── security.py
│
└── requirements.txt
```

---

## ⚙️ Tech Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Authentication**: JWT
* **Password Hashing**: Argon2
* **Server**: Uvicorn

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd vm_manager
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variables

```bash
export DATABASE_URL=postgresql://user:password@localhost/dbname   # Linux/Mac
set DATABASE_URL=postgresql://user:password@localhost/dbname      # Windows
```

---

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

---

## 🌐 API Endpoints

### 🔐 Authentication

| Method | Endpoint    | Description           |
| ------ | ----------- | --------------------- |
| POST   | `/register` | Register new user     |
| POST   | `/login`    | Login & get JWT token |

---

### 🖥️ VM Management (Protected)

> Requires Bearer Token

| Method | Endpoint    | Description   |
| ------ | ----------- | ------------- |
| GET    | `/vms`      | Get all VMs   |
| POST   | `/vms`      | Create new VM |
| GET    | `/vms/{id}` | Get VM by ID  |
| PUT    | `/vms/{id}` | Update VM     |
| DELETE | `/vms/{id}` | Delete VM     |

---

## 🔐 Authentication Flow

1. Register user
2. Login to receive JWT token
3. Pass token in header:

```bash
Authorization: Bearer <your_token>
```

---

## 📊 Logging

* INFO → Normal operations
* WARNING → Unexpected situations
* ERROR → Failures

Logs format:

```
timestamp | level | module | message
```

---

## 🧪 Sample Request

### Create VM

```bash
POST /vms
Authorization: Bearer <token>

{
  "name": "vm-101",
  "status": "running",
  "cpu": 2,
  "memory": 4,
  "os": "linux",
  "region": "india",
  "owner": "team-a"
}
```

---

## 🚧 Future Enhancements

* 🔄 Celery + Redis for async tasks
* 📧 Email notifications
* 📊 Monitoring & metrics (Prometheus/Grafana)
* 🐳 Docker support
* ☁️ AWS deployment (EC2/ECS/EKS)
* 🔁 CI/CD pipeline (GitHub Actions / Jenkins)

---

## 🤝 Contributing

Feel free to fork the repo and submit pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Avinash**
Senior Software Engineer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
