---
meta_title: "Django REST Framework: Creating Your First API"
meta_description: "Learn how to create your first API using Django REST Framework. Step-by-step guide for beginners to build and test a simple API."
meta_keywords: ["Django REST Framework", "Django API tutorial", "Creating API in Django", "Beginner Django API", "Django REST Framework example"]
---

# Django REST Framework: Creating Your First API

Django REST Framework (DRF) is a powerful toolkit for building APIs in Django. Whether you’re creating a small application or a large-scale project, DRF provides the tools to make API development quick and efficient. In this guide, you’ll learn how to create a simple API step-by-step.

---

## Prerequisites

Before starting, make sure you have the following installed:

1. **Python** (3.6+ recommended)
2. **Django** (3.x or later)
3. **Django REST Framework**

You can install Django and DRF using pip:

```bash
pip install django djangorestframework
```

---

## Step 1: Set Up Your Django Project

Start by creating a new Django project and app:

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp api
```

Add the new app to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # Other installed apps
    'rest_framework',
    'api',
]
```

---

## Step 2: Define Your Model

For this tutorial, we’ll create a simple `Book` model.

In `api/models.py`, add the following:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
```

Apply the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 3: Create a Serializer

Serializers in DRF convert complex data types (like model instances) to JSON and vice versa.

In `api/serializers.py`, add:

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

---

## Step 4: Create a ViewSet

ViewSets combine logic for handling HTTP methods (GET, POST, etc.) in a single class.

In `api/views.py`, add:

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

## Step 5: Register Your API Endpoints

DRF provides a `DefaultRouter` class to simplify URL routing.

In `api/urls.py`, add:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Include the `api` app’s URLs in the project’s `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

---

## Step 6: Test Your API

Run the development server:

```bash
python manage.py runserver
```

Visit the API endpoints:

- **List all books:** `http://127.0.0.1:8000/api/books/`
- **Detail for a book:** `http://127.0.0.1:8000/api/books/<id>/`

You can test your API using tools like [Postman](https://www.postman.com/) or the built-in DRF web interface.

---

## Step 7: Extend Your API

You can extend this API by:

1. Adding authentication and permissions using DRF’s built-in features.
2. Filtering or searching with Django Filter or custom logic.
3. Integrating with a frontend using frameworks like React or Angular.

---

## Conclusion

Django REST Framework makes it easy to build robust APIs in Django. By following this guide, you’ve created a simple API that lists, creates, updates, and deletes books. From here, you can expand your API with more advanced features and integrate it into larger projects.

For more tutorials on Django and APIs, check out our [Django Basics Series](#). If you have questions, feel free to leave a comment below!

