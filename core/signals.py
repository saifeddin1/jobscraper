
from core.models import Settings
from core.utils import schedule_scraping_task
from django.db.models.signals import post_save
from django.dispatch import receiver

 
@receiver(post_save, sender=Settings)
def update_task(sender, instance, created, **kwargs):
    print('instance: ', instance.interval_number)
    schedule_scraping_task()
