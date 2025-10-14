from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class ContactUser(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='contacts', on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name or (self.user.get_full_name() if self.user else "ناشناس")
    
    def get_absolute_url(self):
        return reverse('home')