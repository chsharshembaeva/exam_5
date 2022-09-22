from django.db import models
from django.db.models import Count

from account.models import User, Author


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def get_status(self):
        statuses = NewsStatus.objects.filter(news=self)\
            .values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']
        return result

    def __str__(self):
        return f'{self.title} - {self.author.username}'


class Comment(models.Model):
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news')

    def get_status(self):
        statuses = CommentStatus.objects.filter(comment=self) \
            .values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']
        return result

    def __str__(self):
        return f'{self.text} - {self.author.username}'


class Status(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class NewsStatus(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('author', 'news')

    def __str__(self):
        return f'{self.news} - {self.author.username} - {self.status.name}'


class CommentStatus(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('author', 'comment')

    def __str__(self):
        return f'{self.comment} - {self.author.username} - {self.status.name}'







