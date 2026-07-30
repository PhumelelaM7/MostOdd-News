# MostOdd News Application

## Introduction

The MostOdd News Application is a Django web application that I developed as part of my HyperionDev Software Engineering Capstone Project.

The aim of the project was to build a news platform that allows different types of users to perform different tasks based on their roles. Journalists can write articles and newsletters, editors review and approve articles before publication, and readers can browse published content and subscribe to journalists and publishers.

The project also includes a REST API built with Django REST Framework, JWT authentication for secure API access, and MariaDB as the database instead of SQLite.

---

## Features

### User Roles

The application supports three different user roles.

### Reader

Readers can:

- Register and log in
- Read approved articles
- Read newsletters
- Subscribe to journalists
- Subscribe to publishers
- View articles from their subscriptions

Readers cannot:

- Create articles
- Create newsletters
- Approve articles

---

### Journalist

Journalists can:

- Create new articles
- Edit and delete their own articles
- Create newsletters
- Edit and delete their own newsletters

Articles created by journalists are not published immediately. They must first be approved by an editor.

---

### Editor

Editors can:

- View pending articles
- Approve articles
- Edit any article
- Delete any article
- Edit and delete newsletters
- Create publishers

Editors cannot create new articles or newsletters, as these are created by journalists.

---

## Article Approval Process

The application uses an approval workflow before articles become visible to readers.

1. A journalist creates an article.
2. The article is saved with:

```python
approved = False
```

3. The article appears in the Pending Articles page.
4. An editor reviews the article.
5. If approved, the article is updated to:

```python
approved = True
```

6. The approval is recorded in the Approved Article Log.
7. Subscribers receive an email notification about the newly approved article.

---

## Publisher System

Publishers are used to organise journalists and editors.

Each publisher can have:

- Multiple journalists
- Multiple editors
- Multiple articles

Readers are able to subscribe to publishers so they can receive notifications whenever a new article is approved.

---

## Newsletter System

Journalists can create newsletters containing multiple articles.

Readers can browse available newsletters after they have been created.

---

## REST API

The project includes a REST API built using Django REST Framework.

### Articles

Retrieve all approved articles

```
GET /api/articles/
```

Create an article

```
POST /api/articles/
```

Retrieve a specific article

```
GET /api/articles/<id>/
```

Update an article

```
PUT /api/articles/<id>/
```

Delete an article

```
DELETE /api/articles/<id>/
```

---

### Subscribed Articles

Retrieve approved articles from subscribed publishers and journalists.

```
GET /api/articles/subscribed/
```

---

### Newsletters

Retrieve newsletters

```
GET /api/newsletters/
```

Create a newsletter

```
POST /api/newsletters/
```

Retrieve a specific newsletter

```
GET /api/newsletters/<id>/
```

---

### Approved Article Log

Retrieve approval records.

```
GET /api/approved/
```

Create an approval record.

```
POST /api/approved/
```

---

## Authentication

JWT authentication was implemented using Simple JWT.

Obtain an access token:

```
POST /api/token/
```

Refresh an access token:

```
POST /api/token/refresh/
```

---

## Technologies Used

This project was developed using:

- Python
- Django
- Django REST Framework
- MariaDB
- MySQL Client
- JWT Authentication
- HTML
- CSS
- Git
- GitHub

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
```

Navigate to the project folder.

```bash
cd "News Application"
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Run the migrations.

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

Open the application in your browser.

```
http://127.0.0.1:8000/
```

---

## Running the Tests

The project includes automated tests for the API and permissions.

Run all tests with:

```bash
python manage.py test
```

Or run only the API tests.

```bash
python manage.py test news.tests.test_api
```

Current test results:

```
Found 12 test(s)

Ran 12 tests

OK
```

---

## Project Structure

```
News Application/
│
├── news/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── test_api.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│
├── news_project/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Completed Requirements

This project includes:

- Custom User Model
- Reader, Journalist and Editor roles
- MariaDB database
- Django REST Framework API
- JWT Authentication
- Article approval workflow
- Publisher management
- Newsletter management
- Reader subscriptions
- Email notifications
- Approved article logging
- Custom permissions
- Unit tests

---

## Author

**Phumelela Mdingi**
