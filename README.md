# 🧠 Booking API — Enterprise Resource Scheduling & Conflict Resolution System

A production-ready, highly scalable RESTful API designed to manage real-time resource booking (rooms, tables, workspace slots) and eliminate scheduling conflicts. This project is built using a professional **Layered Architecture (Clean Architecture)** to guarantee strict separation of concerns, high testability, and clean code standards.

---

## 🎯 Project Purpose and Business Problems It Solves

In production-grade scheduling systems, naive database implementations lead to business-killing failures. This API is designed specifically to solve critical backend challenges:

- **Strict Overlap & Double-Booking Prevention**: The core engine blocks concurrent booking requests for the same resource. If a slot is taken (e.g., 10:00–12:00), any intersecting request (e.g., 11:00–13:00) is rejected at the service level with appropriate state validation.
- **Race Conditions Control**: Protects resource states from concurrent write operations using robust database transactions and validation mechanisms.
- **Role-Based Access Management (RBAC)**: Enforces clear boundaries between regular users (who browse and book resources) and administrators (who manage resources and system configurations).
- **Stateless & Secure Sessions**: Uses industry-standard token-based authentication to eliminate overhead and ensure secure communication.

---

## 🏗️ Architectural Design (Layered Architecture)

The codebase strictly adheres to enterprise-level separation of concerns, ensuring that database models, business logic, and transport protocols never blend together.

- **API Routing Layer (`app/api/`)**: Handles incoming HTTP requests, coordinates status codes, and injects runtime dependencies.

- **Data Validation Layer (`app/schemas/`)**: Driven by Pydantic V2. Acts as an application-level firewall, ensuring serialization accuracy and input integrity before data touches business engines.

- **Business Logic Layer (`app/services/`)**: The core brain of the system. Implements scheduling algorithms, validation rules, conflict checks, and cryptographic tasks.

- **Data Access Layer (`app/repositories/`)**: Implements the Repository pattern to encapsulate SQLAlchemy queries, shielding the upper layers from raw database operations.

- **Database Model Layer (`app/models/`)**: Contains declarative SQLAlchemy ORM schemas mapping directly to PostgreSQL tables.

---

## 🛠️ Complete Technology Stack

- **Backend Framework**: FastAPI (Core ASGI application)

- **Database**: PostgreSQL (ACID-compliant relational storage)

- **Database Migrations**: SQLAlchemy ORM with Alembic integration

- **Data Serialization & Validation**: Pydantic V2

- **Security & Cryptography**: PyJWT (Tokens) & Bcrypt (Password hashing)

- **Containerization**: Docker & Docker Compose environment

- **Testing Framework**: Pytest with isolated test container

- **CI/CD Automation**: GitHub Actions CI workflow

## 🔐 Authentication and Security Flow

The system implements a professional, stateless authentication flow:

- **User Registration**: The system receives a raw password, processes it through bcrypt with automated salting, and stores only the resulting secure hash in PostgreSQL.

- **User Login**: The server verifies the email and runs a cryptographic match on the password hash. Upon success, it issues a signed asymmetric JWT Access Token.

- **Session Middleware**: Subsequent protected requests require the token passed inside the `Authorization: Bearer <JWT>` header. The system decodes the token on the fly to inject user identity and check system roles (User / Admin).

---

## 📅 Core Booking Logic and Conflict Prevention

The cornerstone of this API is its scheduling integrity validation. When a request to `POST /api/v1/bookings` arrives, `BookingService` evaluates the payload against existing database records using the following mathematical logic:

A new booking request ($Start_{New}$, $End_{New}$) conflicts with an existing booking ($Start_{Existing}$, $End_{Existing}$) if and only if:

$$Start_{New} < End_{Existing} \quad \text{AND} \quad End_{New} > Start_{Existing}$$

If this condition evaluates to true for the selected `resource_id`, the transaction is aborted, and a `400 Bad Request` or `409 Conflict` HTTP exception is raised before the database state can be corrupted.

## 📁 Database Schema and Relationships

The database layer consists of highly optimized tables maintaining relational integrity:

- **`users` Table**: Holds unique email constraints, password_hash, and the role enum field (user, admin).

- **`bookings` Table**: Contains scheduling variables (start_time, end_time), a status field, and foreign key relationships mapping user_id to the users table and resource_id to system assets.

---

## 🧪 Comprehensive Testing Architecture

Software reliability is guaranteed via an automated test suite executed in an isolated runtime environment:

- **Isolated Test DB**: Pytest overrides FastAPI database dependencies to route queries into a temporary PostgreSQL container, ensuring production data remains pristine.

- **Critical Test Coverage (Auth)**: Validates successful user registration, token generation, and rejection of invalid credentials in `test_auth.py`.

- **Critical Test Coverage (Bookings)**: Evaluates standard booking creation, permissions checks, and forcefully triggers edge-case overlapping scenarios to ensure the conflict resolution engine blocks double-bookings in `test_bookings.py`.

---

# 🐳 Docker Containerization Environment

The entire application infrastructure is containerized to achieve environment parity between local development and live servers.

The system can be fully orchestrated with a single command:

```bash
docker compose up --build
```

### 📦 Services

- **backend service** — FastAPI application running with Uvicorn
- **postgres service** — Production-ready PostgreSQL database with persistent volume storage

---

# 📊 Enterprise Logging and Monitoring

The API completely avoids standard Python `print()` statements, relying instead on a structured logging configuration.

### ✅ Features

- **Traceability** — Tracks critical system events such as:
  - User login attempts
  - Authentication failures
  - Blocked booking conflicts

- **Severity Levels**
  - `INFO` — Standard application operations
  - `ERROR` — Unexpected crashes or database failures

This approach ensures cleaner debugging and production-grade observability.

---

# 🚀 CI/CD Automation Pipeline

The entire CI/CD workflow is managed using GitHub Actions.

Every `push` or `pull_request` to the `main` branch automatically triggers:

### ⚙️ Automated Workflow

- ✅ Code linting with `flake8` or `black`
- ✅ Docker infrastructure build
- ✅ Full `pytest` regression test suite
- ✅ Production Docker image build
- ✅ Container registry delivery

---

# 🌍 Live Cloud Deployment

The production API is actively deployed and publicly accessible.

### 🔗 Live Swagger Documentation

```text
https://your-project.onrender.com/docs
```

> Replace the link above with your actual deployment URL.

---

# 💻 How to Install and Run Locally

## 📋 Prerequisites

Before starting, ensure you have installed:

- Python `3.12+`
- PostgreSQL database

---

## ⚡ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/booking-api.git

cd booking-api
```

---

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Development Server

```bash
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

Interactive Swagger UI will be available there.

---

# 🛠️ Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Docker**
- **Pytest**
- **GitHub Actions**
- **Uvicorn**

---

# 📌 Project Highlights

- Fully containerized architecture
- Production-ready PostgreSQL integration
- Automated CI/CD workflow
- Structured enterprise logging
- Interactive Swagger API docs
- Clean modular backend architecture
- Docker-based local and cloud deployment