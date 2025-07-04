from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

import datetime

# Create your models here.

class Profile(models.Model):
    """
    a model to store a user profile, with all its settings, data and preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delete_expired = models.BooleanField("delete expired links", default=False)
    hide_expired = models.BooleanField("hide expired links", default=True)
    default_lifetime = models.DurationField("default link life duration", default=datetime.timedelta(0))

    def __str__(self):
        return str(f"{self.user}'s profile")


class Link(models.Model):
    """
    a model to represent a tracked link shortener with its attributes
    """
    description = models.CharField("description", default="", max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # user who owns the link
    date = models.DateTimeField("date of creation")
    lifetime = models.DurationField("life duration", default=datetime.timedelta(0))  # 0 for unlimited
    destination = models.URLField("url destination", default="https://example.com/", max_length=65535)

    def __str__(self):
        if self.description:
            short_url = self.destination
            if "://" in short_url:
                short_url = short_url.split("://")[1].split("/")[0]
            else:
                short_url = short_url.split("/")[0]
            return f"{self.description} --> {short_url}"
        else:
            return super().__str__()
    
    def url(self):
        """
        returns the absolute url to the shortened link
        """
        path = reverse("redirect_link", args=[self.id])
        domain = Site.objects.get_current().domain
        scheme = "https" if getattr(settings, "SECURE_SSL_REDIRECT", False) else "http"
        return f"{scheme}://{domain}{path}"
    
    @admin.display(
        boolean=True,
        ordering="date",
        description="still active",
    )
    def active(self) -> bool:
        """
        is the link still active, False if expired
        """
        if self.lifetime == datetime.timedelta(0):
            return True
        # return True if the link isn't expired and is not scheduled to be active in the future
        return self.lifetime >= timezone.now() - self.date and self.date <= timezone.now()


class Tracker(models.Model):
    """
    a model to store the informations when a link has been clicked, a link can have multiple trackers
    """
    link = models.ForeignKey(Link, on_delete=models.CASCADE)  # the link from which the tracking originates
    ip = models.GenericIPAddressField("receiver ip", default="0.0.0.0")
    date = models.DateTimeField("date of clicking")
    header = models.TextField("request header", default="")

    def __str__(self):
        return f"{self.ip} | {self.date}"
