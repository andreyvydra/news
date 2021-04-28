from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.forms import ModelForm


class News(models.Model):
    class NewsCategories(models.TextChoices):
        EDUCATION = 'education', 'образование'
        ENTERTAINMENT = 'entertainment', 'развлечение'

    title = models.CharField(max_length=60, verbose_name='Заголовок')
    image = models.ImageField(upload_to='image', verbose_name='Картинка',
                              blank=True)
    text = models.TextField(max_length=1500, verbose_name='Текст новости')
    file = models.FileField(upload_to='file', verbose_name='Файл',
                            blank=True)
    is_urgent = models.BooleanField(default=False, verbose_name='Срочно')
    category = models.CharField(max_length=50, choices=NewsCategories.choices,
                                default=NewsCategories.ENTERTAINMENT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.ManyToManyField("Tag", verbose_name='Тэги')

    def get_tags(self):
        tags_li = self.tags.all()
        res = [i.title for i in tags_li]
        return ', '.join(res)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class NewsForm(ModelForm):
    class Meta:
        model = News


class Tag(models.Model):
    title = models.CharField(max_length=20, verbose_name='Тэг')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
