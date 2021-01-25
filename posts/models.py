from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from tinymce.models import HTMLField
from django.shortcuts import reverse
# Create your models here.



User = get_user_model()

class Author(models.Model):
    author = models.OneToOneField(User,unique=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile pics',default='user.png',blank=True)
    nationality = models.CharField(max_length=100,blank=True)
    birth_date = models.DateField(blank=True)
    birth_place = models.CharField(max_length=100,blank=True)
    biography = models.TextField(blank=True)



    def __str__(self):
        return self.author.username
    

class Catagory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = HTMLField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name='posts')
    thumbnail = models.ImageField(upload_to="gallery")
    catagory = models.ManyToManyField(Catagory,related_name='posts',blank=True)
    approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(null=True, blank=True)
    date_last_updated = models.DateTimeField(auto_now=True)
    previous_post = models.ForeignKey('self',related_name='previous',blank=True,null=True,on_delete=models.SET_NULL)
    next_post = models.ForeignKey('self',related_name='next',blank=True,null=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.pk])
    
    def publish(self):
        self.approved = True
        self.date_published = timezone.now()
    
    def get_catagory(self):
        return self.catagory


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    Post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    
    
    


