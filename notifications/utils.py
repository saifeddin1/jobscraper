from .models import Notification

def create_notification(notification_type, user=None,  data=None):
 
    MAPPING = {
        "new_jobs_added": "New Jobs Added, Check them out!",
        "job_saved": f"<strong>{data.get('job_title') if data else 'Job'}</strong> added to Favorites",
        "job_unsaved": f"<strong>{data.get('job_title') if data else 'Job'}</strong> Removed from Favorites",
        "new_login": "Welcome back! You have logged in successfully.",
    }
    Notification.objects.create(user=user, notification_type=notification_type, message=MAPPING[notification_type])
