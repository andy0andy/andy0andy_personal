from django.db import models
from django.contrib.auth.models import User

# 加工图片
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# 标签
from taggit.managers import TaggableManager

# Create your models here.

# 文章
class ArticlePost(models.Model):
    # 作者，标题，正文，创建时间，更新时间，文章图片
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    title = models.CharField(max_length=100,verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    tags = TaggableManager(blank=True,verbose_name='标签')
    looks = models.IntegerField(default=0,verbose_name='浏览量')
    likes = models.IntegerField(default=0,verbose_name='点赞量')

    created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    # ImageSpecField：从源映像生成新图像,但不保存至数据库
    # ProcessedImageField:不保留原始图像
    title_img = ProcessedImageField(
        upload_to='article_title_img/%Y%m%d/',      # 图片路径
        default='article_title_img/蛋黄君06.jpg',
        processors=[ResizeToFill(200,180),],      # 加工后大小
        format='JPEG',      # 存储格式
        options={'quality':100},        # 图片质量
        verbose_name='标题图片'
    )



    class Meta:
        db_table = 'ArticlePost'
        ordering = '-updated',

    def __str__(self):
        return self.title

