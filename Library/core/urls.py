from django.urls import path
from .views import register, user_login
from .views import PublisherListCreate, PublisherRetrieveUpdateDestroy, \
    AuthorListCreate, AuthorRetrieveUpdateDestroy, \
    BookListCreate, BookRetrieveUpdateDestroy, \
    BookList, TopAuthors
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', csrf_exempt(register), name='register'),
    path('login/', user_login, name='login'),
    path('publishers/', PublisherListCreate.as_view(), name='publisher-list'),
    path('publishers/<int:pk>/', PublisherRetrieveUpdateDestroy.as_view(), name='publisher-detail'),
    path('authors/', AuthorListCreate.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroy.as_view(), name='author-detail'),
    path('books/', BookListCreate.as_view(), name='book-list'),
    path('books_filter/', BookList.as_view(), name='book-list-filter'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroy.as_view(), name='book-detail'),
    path('api/top-authors/', TopAuthors.as_view(), name='top-authors'),
]
