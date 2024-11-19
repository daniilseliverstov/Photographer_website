from django.db import models


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PhotoMainPage(models.Model):
    image = models.ImageField(upload_to='photos_main_page/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or "Photo Main Page"
