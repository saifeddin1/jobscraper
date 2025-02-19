

from core.models import Job, Settings
from core.scrapers import scrape_keejob, scrape_tunisie_travail
from notifications.models import Notification
from notifications.utils import create_notification

from datetime import datetime
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from dateutil.relativedelta import relativedelta

def scrape_all_jobs():
    print('scrape_all_jobs: ........')
    Notification.objects.filter(notification_type="new_jobs_added").delete()
    all_jobs = scrape_keejob() + scrape_tunisie_travail() 

    for job_data in all_jobs:
        if not Job.objects.filter(title__icontains=job_data["title"]).exists():
            Job.objects.create(
                title=job_data["title"],
                description=job_data["description"],
                source_website=job_data["source_website"],
                job_url=job_data["job_url"],
                source_logo=job_data["source_logo"],
                location=job_data["location"],
                company=job_data["company"],
                date_posted=job_data["date_posted"]
            )
    create_notification("new_jobs_added")
    print("done")


def schedule_scraping_task():
    settings = Settings.objects.first()

    settings.refresh_from_db()
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=settings.interval_number or 1,
        period=settings.interval_frequency or 'hours',
    )
    try:
        task = PeriodicTask.objects.get(name='Scrape offers')
        task.start_time = datetime.now() + relativedelta(days=-1)
        task.interval = schedule
        task.save()

    except PeriodicTask.DoesNotExist:
        PeriodicTask.objects.create(
            name='Scrape offers',
            task='core.tasks.scrape_offers',
            start_time=datetime.now() + relativedelta(days=-1),
            interval=schedule,
        )
