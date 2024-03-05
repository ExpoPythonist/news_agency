import uuid
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=60, )

    def __str__(self):
        return self.username


class Agency(models.Model):
    agency_name = models.CharField(max_length=100)
    url = models.URLField()
    agency_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.agency_name
class NewsStory(models.Model):
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia')
    ]

    REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'EU'),
        ('w', 'World')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=20)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news_stories")
    date = models.DateField(default=timezone.now, editable=False)
    details = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "News Stories"

    def __str__(self):
        return f"{self.headline} - {self.author.username}"
