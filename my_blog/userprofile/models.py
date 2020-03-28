from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
# from django.db.models.signals import post_save
# 引入信号接收器的装饰器
# from django.dispatch import receiver
# 处理图片
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    # avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    avatar = ProcessedImageField(
        upload_to='avatar/%Y%m%d/',      # 图片路径
        blank=True,
        processors=[ResizeToFill(40,40),],      # 加工后大小
        format='JPEG',      # 存储格式
        options={'quality':100},        # 图片质量
        verbose_name='标题图片'
    )
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


# 旧教程中采用了信号接收函数，在后台添加User时有时会产生bug
# 已采用其他方法实现其功能，废除了此信号接收函数
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, created, **kwargs):
#     if not created:
#         instance.profile.save(by_signal=True)