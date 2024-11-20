from django.contrib import admin
from .models import Gallery, PhotoMainPage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """
        Админ-класс для управления моделью Gallery в интерфейсе администратора.

        Атрибуты:
            list_display (tuple): Поля модели, которые будут отображаться в списке объектов.
        """
    list_display = ('title', 'created_at')


admin.site.register(PhotoMainPage)
