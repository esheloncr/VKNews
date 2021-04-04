from django.db import models

# Create your models here.


class Article(models.Model):
    text = models.TextField(verbose_name="Текст поста", null=True)
    image = models.TextField(null=True, verbose_name="Изображение")
    date_published = models.DateTimeField(verbose_name="Дата и время создания поста")
    local_post_link = models.IntegerField(verbose_name="ID поста(локальный)")
    post_link = models.TextField(verbose_name="ID поста(глобальный)")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return "Пост"
