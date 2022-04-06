from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=30, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    def __str__(self):
        return '用户名: {}, 密码: {}, 创建时间: {}, 更新时间: {}' \
            .format(self.username, self.password, self.create_time, self.update_time)
