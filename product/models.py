from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField


class Product(models.Model):
    name = models.CharField(max_length=100)


class Profile(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


class Question(models.Model):
    name = models.CharField(max_length=100)
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )
    message = models.CharField(max_length=100)
    required = models.BooleanField()
    type = models.IntegerField()


class Domain(models.Model):
    Name = models.CharField(max_length=100)
    domain_value = JSONField
    result_value = JSONField


class Status(models.Model):
    Name = models.CharField(max_length=100)