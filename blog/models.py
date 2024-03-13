from django.conf import settings 
from django.db import models 
from django.utils import timezone 


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(upload_to='images/', blank=True, null=True, max_length=100) 
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
        

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Email(models.Model):
    sender_name = models.CharField(max_length=100, verbose_name="Vaše meno (povinné)")
    sender_email = models.EmailField(verbose_name="Váš email (povinné)")
    subject = models.CharField(max_length=200, verbose_name="Predmet")
    message = models.TextField(verbose_name="Správa")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject    



    
    


# Create your models here.
