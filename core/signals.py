
from datetime import datetime
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from dateutil.relativedelta import relativedelta


def scrape_offers_task(sender, **kwargs):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,   
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

 