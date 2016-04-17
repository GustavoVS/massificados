from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from product.models import Question


class Sale(models.Model):
    create_timestamp = models.DateField()
    modificate_timestamp = models.DateField()
    email = models.EmailField()


class Deadline(models.Model):
    begin = models.DateField()
    end = models.DateField()
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE
    )


class Detail(models.Model):
    deadline = models.ForeignKey(
        Deadline,
        on_delete=models.CASCADE
    )


class Response(models.Model):
    detail = models.OneToOneField(
        Detail,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    question_value = JSONField
    result_value = JSONField
