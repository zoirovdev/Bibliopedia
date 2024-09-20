from rest_framework import serializers
from authors.serializers import AuthorSerializer
from languages.serializers import LanguageSerializer
from categories.serializers import CategorySerializer
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    published_at = serializers.DateTimeField(ormat="%d %b %Y", read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    authors = AuthorSerializer(many=True)
    languages = LanguageSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"
