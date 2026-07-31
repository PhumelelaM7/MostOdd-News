# MostOdd News Application

## Introduction

The MostOdd News Application is a Django web application that I developed as part of my HyperionDev Software Engineering Capstone Project.

The aim of this project was to build a news website where different users have different responsibilities. Journalists can write articles, editors review and approve them before they are published, and readers can browse approved articles and subscribe to publishers and journalists.

I also added a REST API using Django REST Framework, JWT authentication, MariaDB, Docker support and Sphinx documentation.

---

## Features

The application has three different user roles.

### Reader

Readers can:

- Register and log in
- Read approved articles
- Read newsletters
- Subscribe to publishers
- Subscribe to journalists
- View articles from their subscriptions

Readers cannot create or approve articles.

---

### Journalist

Journalists can:

- Create articles
- Edit and delete their own articles
- Create newsletters
- Edit and delete their own newsletters

Articles created by journalists are saved as pending until an editor approves them.

---

### Editor

Editors can:

- View pending articles
- Approve articles
- Edit pending articles
- Delete pending articles
- Manage publishers
- Manage newsletters

When an article is approved, it is recorded in the Approved Article Log.

---

## Article Approval

When a journalist creates an article it is saved as:

```python
approved = False
```

The article then appears in the Pending Articles page where an editor can review it.

Once the editor approves it, the value changes to:

```python
approved = True
```

The approval is stored in the Approved Article Log and subscribers receive an email notification.

---

## Publisher System

Publishers are used to organise journalists and editors.

Each publisher can have multiple journalists, editors and articles.

Readers can subscribe to publishers so they receive notifications whenever approved articles are published.

---

## Newsletter System

Journalists can create newsletters that contain approved articles.

Readers can browse newsletters from the website.

---

## REST API

The project includes a REST API built with Django REST Framework.

### Articles

```
GET /api/articles/
POST /api/articles/
GET /api/articles/<id>/
PUT /api/articles/<id>/
DELETE /api/articles/<id>/
```

### Subscribed Articles

```
GET /api/articles/subscribed/
```

### Newsletters

```
GET /api/newsletters/
POST /api/newsletters/
GET /api/newsletters/<id>/
```

### JWT Authentication

```
POST /api/token/
POST /api/token/refresh/
```

---

## Technologies Used

I used the following technologies:

- Python
- Django
- Django REST Framework
- MariaDB
- mysqlclient
- JWT Authentication
- Docker
- Docker Compose
- Sphinx
- HTML
- CSS
- Git
- GitHub

---

## Installation

Clone the repository.

```bash
git clone https://github.com/PhumelelaM7/MostOdd-News.git
```

Go into the project folder.

```bash
cd "News Application"
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

Install the project requirements.

```bash
pip install -r requirements.txt
```

---

## Database Setup

This project uses MariaDB instead of SQLite.

Create the database.

```sql
CREATE DATABASE news_application;
```

Create a user.

```sql
CREATE USER 'news_user'@'localhost'
IDENTIFIED BY 'NewsApp123!';
```

Give the user permission to use the database.

```sql
GRANT ALL PRIVILEGES
ON news_application.*
TO 'news_user'@'localhost';

FLUSH PRIVILEGES;
```

If you use different database details, update the `DATABASES` section inside:

```
news_project/settings.py
```

Run the migrations.

```bash
python manage.py migrate
```

Create a superuser.

```bash
python manage.py createsuperuser
```

Start the server.

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Running with Docker

Build the project.

```bash
docker compose build
```

Run the containers.

```bash
docker compose up
```

Apply migrations.

```bash
docker compose exec web python manage.py migrate
```

Create a superuser.

```bash
docker compose exec web python manage.py createsuperuser
```

Open:

```
http://localhost:8000/
```

---

## Running the Tests

Run all tests.

```bash
python manage.py test
```

Or only the API tests.

```bash
python manage.py test news.tests.test_api
```

Current result:

```
Found 12 tests

Ran 12 tests

OK
```

---

## Documentation

The project also includes Sphinx documentation.

Generate it using:

```bash
cd docs
make html
```

Open:

```
docs/build/html/index.html
```

---

## Project Structure

```
News Application/

├── docs/
├── news/
├── news_project/
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Completed Features

This project includes:

- Custom User Model
- Reader, Journalist and Editor roles
- Publisher management
- Reader subscriptions
- Article approval workflow
- Newsletter management
- Approved Article Log
- Email notifications
- REST API
- JWT Authentication
- MariaDB
- Docker support
- Sphinx documentation
- Unit tests

---

## Author

Phumelela Mdingi
