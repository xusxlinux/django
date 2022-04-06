from django.db import models
from user.models import User


# Create your models here.


class Notes(models.Model):
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '标题: {} 内容:{} 创建时间: {} 修改时间: {}'\
            .format(self.title, self.content, self.create_time, self.update_time)