from django.contrib import admin
from .models import Gallery, PhotoMainPage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


admin.site.register(PhotoMainPage)
