from django.core.management.base import BaseCommand
from scraper.scraper import scrape_all_jobs

class Command(BaseCommand):
    help = "Scrape job offers from specified websites"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the scraping process...")
        scrape_all_jobs()
        self.stdout.write("Scraping process finished.")
