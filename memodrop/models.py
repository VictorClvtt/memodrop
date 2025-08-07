from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    class ProfileColor(models.TextChoices):
        BLACK = 'black', 'Black'
        RED = 'red', 'Red'
        PINK = 'pink', 'Pink'
        GREEN = 'green', 'Green'
        BLUE = 'blue', 'Blue'
        YELLOW = 'yellow', 'Yellow'
    profile_color = models.CharField(
        max_length=10,
        choices=ProfileColor.choices,
        default=ProfileColor.BLACK
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'

class Friendship(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_sent')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_received')
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

class Memo(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memo_sent')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memo_received')
    content = models.TextField()
    image = models.ImageField(upload_to='memos/', blank=True, null=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_1', 'user_2', 'date'],
                name='unique_memo_per_day'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'Memo from {self.user_1.username} to {self.user_2.username} on {self.date}'