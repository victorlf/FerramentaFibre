from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Account(models.Model):
    year = models.CharField(max_length=200)
    sales = models.CharField(max_length=200)


class Signal(models.Model):
    name = models.TextField(max_length=200)
    adress = models.TextField(max_length=200)
    quality = models.TextField(max_length=200)
    signal = models.TextField(max_length=200)
    channel = models.TextField(max_length=200)
    encryption = models.TextField(max_length=200)
    time = models.TextField(max_length=200)

    def __str__(self):
        return self.signal + '  -  ' + self.time
