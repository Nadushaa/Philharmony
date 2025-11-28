from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Менеджер'),
        ('artist', 'Артист'),
        ('admin', 'Администратор'),
    ]
    
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='artist')
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_artist(self):
        return self.role == 'artist'
    
    def is_admin(self):
        return self.role == 'admin'