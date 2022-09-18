from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField('Title', max_length=100)
    text = models.TextField()
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.category} :: {self.title}'

    def get_absolute_url(self):
        return f'/gamedesk/{self.id}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    upload = models.FileField(upload_to='uploads/')


class Category(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildmaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кодевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    name = models.CharField(max_length=50, choices=TYPE, default='tank')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1600)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField('Approved', null=True, blank=True)

    def __str__(self):
        return f'{self.author} - {self.dateCreation}'


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
