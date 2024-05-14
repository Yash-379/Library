from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Publisher, Author, Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        publisher_data = validated_data.pop('publisher')

        # Create Author instance
        author_instance = Author.objects.create(**author_data)

        # Create Publisher instance
        publisher_instance = Publisher.objects.create(**publisher_data)

        # Create Book instance with author and publisher
        book_instance = Book.objects.create(author=author_instance, publisher=publisher_instance, **validated_data)

        return book_instance

    def update(self, instance, validated_data):
        # Update the title field
        instance.title = validated_data.get('title', instance.title)

        # Update the author field if provided
        author_data = validated_data.get('author')
        if author_data:
            author_instance = instance.author
            author_instance.name = author_data.get('name', author_instance.name)
            author_instance.save()

        # Update the publisher field if provided
        publisher_data = validated_data.get('publisher')
        if publisher_data:
            publisher_instance = instance.publisher
            publisher_instance.name = publisher_data.get('name', publisher_instance.name)
            publisher_instance.save()

        instance.save()
        return instance
