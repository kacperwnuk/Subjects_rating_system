from django.db import models
import datetime


class Subject(models.Model):
    fullname = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10)
    tutor = models.CharField(max_length=100)
    basic_info = models.TextField(max_length=300)


class Opinion(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    date = models.DateField(default=datetime.date.today)
    rating = models.FloatField()
