from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Author, Publisher, Book


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'navneet_test1',
            'password': 'navneet'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_login_success(self):
        response = self.client.post(reverse('login'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_failure(self):
        invalid_credentials = {
            'username': 'wronguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_data = {'name': 'Test Author'}

    def test_create_author(self):
        response = self.client.post(reverse('author-list'), self.author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'Test Author')

    def test_retrieve_author(self):
        author = Author.objects.create(name='Test Author')
        response = self.client.get(reverse('author-detail', kwargs={'pk': author.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')

    def test_update_author(self):
        author = Author.objects.create(name='Test Author')
        updated_author_data = {'name': 'Updated Test Author'}
        response = self.client.put(reverse('author-detail', kwargs={'pk': author.id}), updated_author_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get(id=author.id).name, 'Updated Test Author')


class PublisherCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.publisher_data = {'name': 'Test Publisher'}

    def test_create_publisher(self):
        url = reverse('publisher-list')
        response = self.client.post(url, self.publisher_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 1)
        self.assertEqual(Publisher.objects.get().name, 'Test Publisher')

    def test_retrieve_publisher(self):
        publisher = Publisher.objects.create(name='Test Publisher')
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Publisher')

    def test_update_publisher(self):
        publisher = Publisher.objects.create(name='Test Publisher')
        updated_publisher_data = {'name': 'Updated Test Publisher'}
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.put(url, updated_publisher_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Publisher.objects.get(id=publisher.pk).name, 'Updated Test Publisher')

    # def test_delete_publisher(self):
    #     publisher = Publisher.objects.create(name='Test Publisher')
    #     url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Publisher.objects.filter(id=publisher.pk).exists())


class BookCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book_data = {
            "title": "Example Book",
            "author": {
                "id": 1,
                "name": "Author Name"
            },
            "publisher": {
                "id": 1,
                "name": "Publisher Name"
            }
        }

    def test_create_book(self):
        url = reverse('book-list')
        # breakpoint()
        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().title, self.book_data['title'])  # Compare with the provided book_data

    def test_retrieve_book(self):
        book = Book.objects.create(title='Test Book', author=self.author, publisher=self.publisher)
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book(self):
        book = Book.objects.create(title='Test Book', author=self.author, publisher=self.publisher)
        updated_book_data = {
            'title': 'Updated Test Book',
            'author': {
                'id': self.author.id,
                'name': self.author.name
            },
            'publisher': {
                'id': self.publisher.id,
                'name': self.publisher.name
            }
        }
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.put(url, updated_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=book.pk).title, 'Updated Test Book')


class CustomPermissionsTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a book
        self.book = Book.objects.create(title='Example Book')

    def test_authenticated_user_access(self):
        # Test that authenticated users can access certain endpoints

        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Access the endpoint that requires authentication
        url = reverse('book-list')  # Example URL for a list of books
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_user_actions(self):
        # Test that only authorized users can perform certain actions

        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Attempt to delete the book
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)

        # Check that the response status code is 403 Forbidden (since the user is not an admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_access(self):
        # Test that unauthorized users receive appropriate error messages or status codes

        # Logout any existing user
        self.client.logout()

        # Access the endpoint that requires authentication
        url = reverse('book-list')  # Example URL for a list of books
        response = self.client.get(url)

        # Check that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)