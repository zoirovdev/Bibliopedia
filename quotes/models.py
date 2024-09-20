from django.db import models

from users.models import User
from books.models import Book

class Quote(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='quote_users', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='quote_books', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return " ".join(self.content.split()[3])+"..."