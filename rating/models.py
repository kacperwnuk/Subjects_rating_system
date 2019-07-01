from django.contrib.auth.models import User as AuthUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime

from django.db.models import Avg
from django.urls import reverse


class User(models.Model):
    basic_info = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    @property
    def avg_rating(self):
        return Opinion.objects.filter(user=self).aggregate(Avg('rating'))['rating__avg'] or 'Nie oceniłeś jeszcze żadnego przedmiotu'

    def __str__(self):
        return self.basic_info.username


class Subject(models.Model):
    fullname = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10)
    tutor = models.CharField(max_length=100)
    basic_info = models.TextField(max_length=300)

    @property
    def rating(self):
        return self.opinion_set.all().aggregate(Avg('rating'))['rating__avg'] or 'Brak oceny'

    def __str__(self):
        return self.shortcut


class Opinion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    date = models.DateField(default=datetime.date.today)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def get_absolute_url(self):
        return reverse('rating:opinion', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
