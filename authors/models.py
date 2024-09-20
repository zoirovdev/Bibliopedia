from django.db import models

from users.models import User

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='author_photos/', null=True, blank=True)

    user = models.ForeignKey(User, related_name='author_users', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.full_name