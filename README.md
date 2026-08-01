# MostOdd News Application

## Introduction

The MostOdd News Application is a Django web application that I developed as part of my HyperionDev Software Engineering Capstone Project.

The aim of this project was to build a news website where different users have different responsibilities. Journalists create articles, editors review and approve them before publication, and readers browse approved articles while subscribing to publishers and journalists that interest them.

The project also includes a REST API built with Django REST Framework, JWT authentication, MariaDB, Docker support, Sphinx documentation, and automated API tests.

---

## Features

The application provides role-based access control through three different user roles.

### Reader

Readers can:

- Register and log in
- Read approved articles
- Read newsletters
- Subscribe to publishers directly from the article list or article detail page
- Subscribe to journalists directly from the article list or article detail page
- View articles from subscribed publishers and journalists

Readers cannot create, edit, delete or approve articles.

---

### Journalist

Journalists can:

- Create articles
- Edit their own articles
- Delete their own articles
- Create newsletters
- Edit their own newsletters
- Delete their own newsletters

Articles created by journalists remain pending until approved by an editor.

---

### Editor

Editors can:

- View pending articles
- Approve articles
- Edit any article
- Delete any article
- Create publishers
- Manage newsletters

The home page provides quick access to:

- Read Articles
- Create Publisher
- Pending Articles

making the editorial workflow more efficient.

---

## Role-Based User Management

The application uses a custom user model with three roles:

- Reader
- Journalist
- Editor

Reader accounts may subscribe to publishers and journalists.

If a Reader changes role to either Journalist or Editor, the application automatically removes all reader subscriptions to ensure role-specific data remains consistent.

Users are automatically assigned to the correct Django Group during registration based on their selected role.

---

## Article Approval Workflow

When a journalist creates an article it is initially saved as:

```python
approved = False
```

The article appears on the Pending Articles page where editors can review it.

Once approved, the article becomes:

```python
approved = True
```

The application then:

- Records the approval in the Approved Article Log
- Sends email notifications to subscribers
- Triggers the internal API integration used by the project

---

## Publisher System

Publishers organise journalists and editors.

Each publisher can contain multiple:

- Journalists
- Editors
- Articles

Editors can create publishers directly from the application interface.

Readers can subscribe to publishers to receive updates whenever approved articles are published.

---

## Newsletter System

Journalists create newsletters containing approved articles.

Editors can also manage newsletters.

Readers can browse all published newsletters.

---

## REST API

The project includes a REST API built with Django REST Framework.

### Articles

```
GET    /api/articles/
POST   /api/articles/
GET    /api/articles/<id>/
PUT    /api/articles/<id>/
DELETE /api/articles/<id>/
```

### Subscribed Articles

```
GET /api/articles/subscribed/
```

### Newsletters

```
GET    /api/newsletters/
POST   /api/newsletters/
GET    /api/newsletters/<id>/
```

### JWT Authentication

```
POST /api/token/
POST /api/token/refresh/
```

---

## Technologies Used

This project was developed using:

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

Navigate into the project folder.

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

Create a database user.

```sql
CREATE USER 'news_user'@'localhost'
IDENTIFIED BY 'NewsApp123!';
```

Grant privileges.

```sql
GRANT ALL PRIVILEGES
ON news_application.*
TO 'news_user'@'localhost';

FLUSH PRIVILEGES;
```

If your database credentials differ, update the `DATABASES` section inside:

```
news_project/settings.py
```

Run migrations.

```bash
python manage.py migrate
```

Create a superuser.

```bash
python manage.py createsuperuser
```

Run the development server.

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Running with Docker

Build the containers.

```bash
docker compose build
```

Start the application.

```bash
docker compose up
```

Run migrations.

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

Run only the API tests.

```bash
python manage.py test news.tests.test_api
```

---

## Documentation

Sphinx documentation is included.

Generate the documentation using:

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

- Custom User Model
- Role-based Authentication
- Automatic Django Group Assignment
- Automatic Reader Subscription Cleanup on Role Change
- Publisher Management
- Reader Subscriptions
- Article Approval Workflow
- Newsletter Management
- Approved Article Log
- Email Notifications
- REST API
- JWT Authentication
- MariaDB Integration
- Docker Support
- Sphinx Documentation
- Automated API Tests
- Role-Based Access Control
- Improved User Interface for Editors and Readers

---

## Improvements After Reviewer Feedback

The project was enhanced following reviewer feedback by implementing the following improvements:

- Journalists can edit and delete their own articles.
- Editors can edit and delete all articles.
- Editors can create publishers directly from the application.
- Reader subscription actions are available directly from the article list, improving usability.
- Editor shortcuts for **Create Publisher** and **Pending Articles** are displayed prominently on the home page.
- Reader subscriptions are automatically removed when a user's role changes from Reader to Journalist or Editor, ensuring role-specific data remains consistent.

---

## Author

**Phumelela Mdingi**