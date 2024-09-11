from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating =  self.posts.aggregate(pr=Coalesce(Sum('rating'),0))['pr']
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'),0))['cr']
        posts_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('rating'),0))['pcr']

        print(posts_rating)
        print('-------------------')
        print(comments_rating)
        print('-------------------')
        print(posts_comments_rating)


        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новости'),
    ]

    post_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_type = models.CharField(max_length=2, choices=POSITIONS, default=news)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        small_text = self.text[0:124] + '...'
        return small_text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()








