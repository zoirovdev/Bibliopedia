from rest_framework import serializers

from .models import Book

class BookSerializer(serializers.ModelSerializer):
    published_at = serializers.DateTimeField(ormat="%d %b %Y", read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Book
        fields = "__all__"
        