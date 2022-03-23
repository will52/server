import imp
from turtle import title
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Prof (models.Model):
    name = models.CharField(max_length=64)
    profID = models.CharField(max_length=3,unique=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    title = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    semester = models.CharField(max_length=1)
    modID = models.CharField(max_length=3,null=True)
    profs = models.ManyToManyField(Prof, related_name="modules")

    def __str__(self):
        return self.title

class Rating (models.Model):
    user = models.ForeignKey (User, on_delete= models.CASCADE)
    val = models.PositiveIntegerField (default=5, validators=[MaxValueValidator(5),MinValueValidator(1)])
    prof = models.ForeignKey (Prof, on_delete= models.CASCADE)
    module = models.ForeignKey (Module, on_delete= models.CASCADE)