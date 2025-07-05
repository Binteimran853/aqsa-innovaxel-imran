from django.db import models
import string
import random

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class URL(models.Model):
    url = models.URLField()
    shortCode = models.CharField(max_length=10, unique=True, default=generate_shortcode)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)  # ✅ auto-update on save()

    accessCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.shortCode
