from rest_framework import serializers
from authors.serializers import AuthorSerializer
from languages.serializers import LanguageSerializer
from categories.serializers import CategorySerializer
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    published_at = serializers.DateTimeField(format="%d %b %Y")
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Book
        fields = "__all__"
