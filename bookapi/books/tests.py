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

    def test_update_book(self):
        updated_data = {TITLE: 'Updated Title',
                        AUTHOR: 'Test Author',
                        RELEASE_YEAR: 1999}
        response = self.client.put(self.detail_url,
                                   updated_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_partial_update_book_title(self):
        response = self.client.patch(self.detail_url,
                                     {TITLE: 'Partially Updated Title'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Partially Updated Title')

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_create_book_missing_title_returns_400(self):
        data = {AUTHOR: 'Test Author', RELEASE_YEAR: 2020}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
