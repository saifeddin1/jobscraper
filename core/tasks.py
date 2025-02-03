from core.scrapers import scrape_all_jobs
from jscraper.celery import app


@app.task
def scrape_offers():
    print("----------- Scraping task ----------")
    scrape_all_jobs()
