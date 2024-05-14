from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed


class Author(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # Add other fields as needed
