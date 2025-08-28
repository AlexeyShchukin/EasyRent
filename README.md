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

## Features

### Listings
- **Landlords** can:  
  - view all listings or only their own, 
  - update and delete their own listings.  
- **All users** can:  
  - view the list of all listings,  
  - retrieve a specific listing by its **ID**.  
- A listing retrieved by **ID** returns the full object, including the number of views.

### Bookings
- When fetching all bookings for a specific listing **Renters** and **unauthenticated users**
only receive booking dates with the **Confirmed** status. 
On the frontend, these are displayed as a calendar with unavailable dates.
- **Renters** can retrieve full booking objects for:  
  - all their own bookings,
  - their bookings for a specific listing.
- **Landlords** can retrieve full booking objects only for their **own listings**.
- Both **renters** and **landlords** can retrieve a full booking object by **ID** 
(with the related listing via `select_related`), provided they are either:  
  - the booking’s renter, or  
  - the owner of the listing.  
- **Renters** can:  
  - create bookings and update booking dates:
    - overlapping dates are prevented,  
    - past dates cannot be booked,  
    - `end_date` cannot be earlier than `start_date`
  - cancel their bookings (**status → Cancelled**):  
    - only up to **2 days before check-in**.
- **Landlords** can only update booking status to:  
  - **Rejected** (only if the current status is Pending),  
  - **Confirmed** (only if the current status is Pending),
  - **Completed** (only if the current status is Confirmed and not before the **day of check-out**).
  
### Reviews
- A **renter** can leave **one review and rating per listing**, but only after completing their stay (**status = Completed**).  
- Renters may later update their rating or comment.  
- **All users** can view reviews and the average rating.  
- A **renter** can view their own review for a specific listing.  

### Views and Queries Counting
- When retrieving a specific listing or submitting a search query,
**view counting** and **search query counting** are handled in a separate process using background tasks to:  
  - avoid blocking the main process,  
  - preserve idempotency.
- **View counting** tracks unique views per listing.  
  - A unique user is identified by their **user ID**, or by **session ID** if the user is not authenticated.  
  - Only **one view per user/session per listing per day** is recorded.
- **Query normalization** is applied to reduce duplicates and ensure consistency.  
- The database stores **normalized queries** instead of many near-identical ones.  
- A **counter** for each unique normalized query will be added.  

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
