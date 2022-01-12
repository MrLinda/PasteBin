from django.db import models


class database(models.Model):
    text = models.CharField(max_length=1000)  # 文本信息
    index = models.BigIntegerField()  # 索引（用随机数）
    delete = models.IntegerField(default=0)  # 阅后即焚
    date = models.IntegerField(default=0)  # 过期日期
    password = models.CharField(max_length=16, default='d41d8cd98f00b204e9800998ecf8427e')  # 以16位md5存的密码（在前端进行加密）
