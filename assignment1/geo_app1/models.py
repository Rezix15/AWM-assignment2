from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.db import models

# Create your models here
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # modified = models.DateTimeField(auto_now_add=True, editable=False)

    location = models.PointField(editable=False, blank=True, null=True, default=None)

    objects = models.Manager()

    def __str__(self):
        return str(self.location)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Hotel(models.Model):
    name = models.CharField(max_length=255, null=True)
    location = models.PointField(default=None)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=200, null=True)
    website = models.URLField(null=True)
    wheelchair = models.CharField(max_length=10, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=True)
    cuisine = models.CharField(max_length=255, null=True)
    location = models.PointField(default=None)
    opening_hours = models.CharField(max_length=255, null=True)
    website = models.URLField(null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    wheelchair = models.CharField(max_length=10, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Park(models.Model):
    name = models.CharField(max_length=255, null=True)
    location = models.PointField(default=None)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Library(models.Model):
    name = models.CharField(max_length=255, null=True)
    location = models.PointField(default=None)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=200, null=True)
    website = models.URLField(null=True)
    wheelchair = models.CharField(max_length=10, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
