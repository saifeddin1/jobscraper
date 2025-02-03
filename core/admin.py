from django.contrib import admin
from .models import Job
from .scrapers import scrape_all_jobs

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_website')
    actions = ['scrape_jobs']

    def scrape_jobs(self, modeladmin, queryset):
        """
        Scrape jobs from the selected sources.
        """
        scrape_all_jobs()
