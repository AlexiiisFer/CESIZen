from django.db import models
from django.contrib.auth.models import User
import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default/user_logo.png')

    def __str__(self):
        return self.user.username
  
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Nom de l'icône (ex: 'fa-spa', 'fa-brain')")

    def __str__(self):
        return self.name

class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='activity_images/', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='activities')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField(blank=True, null=True, help_text="Lien vers une vidéo (YouTube, Vimeo...)")

    def save(self, *args, **kwargs):
        if self.video_url and "youtube.com/watch" in self.video_url:
            self.video_url = self.convert_to_embed(self.video_url)
        super().save(*args, **kwargs)

    def convert_to_embed(self, url):
        pattern = r"watch\?v=([a-zA-Z0-9_-]+)"
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        return url

    def __str__(self):
        return self.title
    
class FavoriteActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.activity.title}"

    
class Information(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.title