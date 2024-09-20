from django.db import models

from users.models import User

class Language(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='language_users', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name