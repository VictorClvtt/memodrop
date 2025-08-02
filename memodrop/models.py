from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'

class Friendship(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_sent')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.IntegerChoices):
        PENDING = 0
        ACCEPTED = 1
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_1', 'user_2'],
                name='unique_friendship'
            )
        ]
    
    def clean(self):
        if self.user_1 == self.user_2:
            raise ValidationError("Usuário não pode ser amigo de si mesmo.")
