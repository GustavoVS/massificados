from __future__ import unicode_literals

from django.db import models


class FileType(models.Model):
    name = models.CharField(max_length=20)


class Status(models.Model):
    name = models.CharField(max_length=100)
