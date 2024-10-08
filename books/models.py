from django.db import models

from users.models import User
from authors.models import Author
from categories.models import Category
from languages.models import Language

class Book(models.Model):
    title = models.CharField(200)
    definition = models.TextField()
    published_at = models.DateTimeField()
    image = models.ImageField(upload_to='book_photos/', null=True, blank=True)

    user = models.ForeignKey(User, related_name='book_users', on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    language = models.ForeignKey(Language, related_name='book_languages', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title