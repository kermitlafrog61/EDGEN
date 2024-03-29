from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify

from .tasks import send_news

User = get_user_model()


class News(models.Model):
    slug = models.SlugField(primary_key=True, max_length=150, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    university = models.ForeignKey(
        'university.University', on_delete=models.CASCADE, related_name='news')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + \
                datetime.now().strftime('_%d_%M_%H')
        return super().save(*args, **kwargs)


class NewsRating(models.Model):
    RATES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='news_rating')
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='rating')
    rate = models.PositiveSmallIntegerField(choices=RATES)

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'Рейтинг новости'
        verbose_name_plural = 'Рейтинги новостей'
        unique_together = ['user', 'news']


class NewsComment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='news_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='news_comments')

    class Meta:
        verbose_name = 'Комментарий новости'
        verbose_name_plural = 'Комментарии новостей'

    def __str__(self) -> str:
        return f'Комментарий от {self.user.username}'


@receiver(post_save, sender=News)
def send_news_created(sender: News, instance: News, created: bool, **kwargs):
    if created:
        recipients_list = [
            student.email for student in instance.university.students.all()]
        send_news.delay(
            recipient_list=recipients_list,
            university_id=instance.university.id,
            news_id=instance.slug
        )
