
from datetime import datetime
from core.models import Settings
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

settings = Settings.objects.first()

def scrape_offers_task(sender, **kwargs):
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

 

@receiver(post_save, sender=Settings)
def update_task(sender, instance, created, **kwargs): 
    print('instance: ', instance.interval_number)
    scrape_offers_task(sender)