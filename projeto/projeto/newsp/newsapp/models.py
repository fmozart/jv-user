from django.db import models
from shortuuid.django_fields import ShortUUIDField 
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django

from django.utils import timezone
from PIL import Image

class Category(models.Model):
    title=models.CharField(max_length=200)
    category_image=models.ImageField(upload_to='imgs/')

    class Meta:
        verbose_name_plural ='Categories'

    def __str__(self):
        return self.title

class News(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='Imgs')
    detail = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural ='News'

    def __str__(self):
        return self.title
        

class Comment(models.Model):
    news = models.ForeignKey(News,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    comment = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='avatar.jpg',
        upload_to='profile_avatars' 
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
       
        super().save(*args, **kwargs)

        
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)

            img.thumbnail(output_size)

            img.save(self.avatar.path)