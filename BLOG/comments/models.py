from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from article.models import ArticlePost

# Create your models here.

class Comments(models.Model):

    article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,verbose_name='文章')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='评论者')

    body = RichTextField(verbose_name='评论')
    created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        db_table = 'Comments'
        ordering = ['-created']

    def __str__(self):
        return self.body