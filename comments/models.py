from django.db import models

from books.models import Book
from users.models import User

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='comment_users', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comment_books', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return " ".join(self.content.split()[3])+"..."
