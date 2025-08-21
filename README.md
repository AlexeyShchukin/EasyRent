# EasyRent API

**EasyRent** is a housing rental platform built with **Django Rest Framework**.  
It provides a RESTful API that allows users to publish rental listings (as landlords) and book accommodations (as tenants).

---

## Tech Stack

- **Python**: 3.13+
- **Django**: 5.2.5+
- **Django REST Framework**: 3.16.1+
- **MySQL**: 8.0+
- **Docker & Docker Compose**: Containerization and service orchestration
- **Gunicorn**: WSGI server for production

---

## Installation & Setup

The project uses **Docker** and **Docker Compose** for simplified deployment.

### 1. Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/)
- Install [Docker Compose](https://docs.docker.com/compose/)

### 2. Clone the repository
```
git clone https://github.com/AlexeyShchukin/EasyRent.git
cd EasyRent
```

### 3. Configure environment variables

Create a .env file in the project root based on env.example.
```
# .env

# Django settings
SECRET_KEY=your_secret_key_here
DEBUG=True

# Database settings
DB_HOST=db
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_pass
DB_NAME=easy_rent
```

### 4. Build and run the project
```
docker-compose up -d --build
```
This will:  
Build Docker images  
Start the db  
Apply database migrations  
Set basic groups with permissions
Start app  

### 5. Accessing the API
After startup, the API is available at: http://localhost:8000/api/
