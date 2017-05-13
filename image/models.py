from django.db import models
from django.utils import timezone


class Image(models.Model):

    file = models.ImageField('画像', upload_to='img/')
    names = models.CharField('映っているキャラ達', max_length=255)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.names
