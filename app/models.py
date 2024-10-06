from django.db import models
from django.contrib.auth.models import User


class Seed(models.Model):
    name = models.CharField(max_length=300)


class Field(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    area = models.DecimalField(max_digits=6, decimal_places=3)
    longtitude = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    soil_type = models.CharField(max_length=255, null=True, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    seeds = models.ManyToManyField(Seed, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


