import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Person(AbstractUser):
    profileId = models.CharField(max_length=255, default=str(uuid.uuid4()))
    birthdate = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comments.all()

    def add_comment(self, author, content):
        return self.comments.create(author=author, content=content)

    def delete_comment(self, comment_id):
        comment = self.comments.filter(pk=comment_id).first()
        if comment:
            comment.delete()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.email} on {self.post.title}'