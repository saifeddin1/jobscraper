from django.db import models
from django.utils.timezone import now
from users.models import CustomUser  # Import the user model

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("new_jobs_added", "New Jobs Added"),
        ("job_saved", "Job Saved Successfully"),
        ("job_unsaved", "Job Unsaved"),
        ("new_login", "New Login"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications", null=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification : {self.get_notification_type_display()}"
