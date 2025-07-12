# Learning Django

## Step 1: Install Python & create virtual environment

Make sure to have `Python 3.8+` installed.

**Navigate to the folder where you want your project**

`cd path\to\your\folder`

**Create virtual env**

`python -m venv venv`

**Activate virtual env**

`venv\Scripts\activate` (Windows)

## Step 2: Install Django and DRF

`pip install django djangorestframework`

## Step 3: Start Django project & app

**Start project**

`django-admin startproject bookapi`

`cd bookapi`

**Start app**

`python manage.py startapp books`

## Step 4: Add to settings
**Open `bookapi/settings.py` in VS Code.**

In `INSTALLED_APPS`, add:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'books',
]
```

## Step 5: Create model
In `books/models.py`:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.author} ({self.release_year})'
```

## Step 6: Make migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Create serializer

In `books/serializers.py`:

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

## Step 8: Create views (CRUD)

In `books/views.py`:

```python
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

## Step 9: Create URLs

In `books/urls.py`:

```python
from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
```

Then, in `bookapi/urls.py`, add:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
]
```

## Step 10: Run server

`python manage.py runserver`

**Open your browser and go to:**

http://127.0.0.1:8000/api/books/ → to GET all books or POST new book\
http://127.0.0.1:8000/api/books/1/ → to GET, PUT, PATCH, DELETE a specific book

## Step 11: Write unit tests

In `books/tests.py`:

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book

TITLE = 'title'
AUTHOR = 'author'
RELEASE_YEAR = 'release_year'

class BookAPITests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Title',
                                        author='Test Author',
                                        release_year=2025)
        self.list_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail', args=[self.book.id])

    def test_create_book(self):
        data = {TITLE: 'Some Book Title',
                AUTHOR: 'John Smith',
                RELEASE_YEAR: 2019}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest('id').title, data[TITLE])

    def test_read_books_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Book.objects.count())

    def test_read_single_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[TITLE], self.book.title)
```

**Run tests:**

`python manage.py test`