from __future__ import unicode_literals

from django.db import models


class FileType(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name