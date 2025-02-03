from django.db import models
from django.utils.timezone import now


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    company = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    source_logo = models.URLField(blank=True, null=True)
    source_website = models.CharField(max_length=100)
    job_url = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.CharField(max_length=255, blank=True, null=True)
    scraped_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Settings(models.Model):
    FREQUENCY_CHOICES = [
        ("hours", "Hours"),
        ("minutes", "Minutes"),
        ("seconds", "Seconds"),
        ("days", "Days"),
    ]

    interval_number = models.IntegerField(default=1)
    interval_frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, default="hours"
    )
