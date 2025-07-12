from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestoryView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestoryView.as_view(), name='book-detail'),
]