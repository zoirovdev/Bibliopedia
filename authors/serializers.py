from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = Author
        fields = "__all__"