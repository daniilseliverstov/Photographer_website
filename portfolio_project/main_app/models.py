from django.db import models


class Gallery(models.Model):
    """
        Модель для представления галереи изображений.

        Атрибуты:
            title (str): Название галереи, максимальная длина 200 символов.
            description (str): Описание галереи.
            created_at (datetime): Дата и время создания галереи, автоматически устанавливается при добавлении.
        """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
                Возвращает строковое представление объекта Gallery.

                Returns:
                    str: Название галереи.
                """
        return self.title


class PhotoMainPage(models.Model):
    """
        Модель для представления фотографий на главной странице.

        Атрибуты:
            image (ImageField): Изображение, загружаемое в папку 'photos_main_page/'.
            caption (str): Подпись к изображению, может быть пустой.
        """
    image = models.ImageField(upload_to='photos_main_page/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
                Возвращает строковое представление объекта PhotoMainPage.

                Returns:
                    str: Подпись к изображению или "Photo Main Page", если подпись отсутствует.
                """
        return self.caption or "Photo Main Page"
