import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from notifications.models import Notification
from notifications.utils import create_notification
from .models import Job


def scrape_keejob():
    url = "https://www.keejob.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_cards = soup.find_all('div', class_='block_white')

    jobs = []
    for job_element in job_cards:
        title_tag = job_element.find("h6").find("a")
        title = title_tag.text.strip() if title_tag else None
        description = job_element.find("div", class_="span9").text.strip().split("\n")[
            1] if job_element.find("div", class_="span9") else None
        company = job_element.find("div", class_="meta_a").find(
            "a").text.strip() if job_element.find("div", class_="meta_a") else None
        location = job_element.find("i", class_="fa fa-map-marker").next_sibling.strip(
        ) if job_element.find("i", class_="fa fa-map-marker") else None

        # Extract source logo and construct full URL
        logo_tag = job_element.find("figure").find(
            "img") if job_element.find("figure") else None
        source_logo = url + \
            logo_tag["src"] if logo_tag and logo_tag.has_attr("src") else None

        date_posted = None
        jobs.append({
            'title': title,
            'description': description,
            'company': company,
            'location': location,
            'source_logo': source_logo,
            'source_website': "Keejob",
            'job_url': title_tag.get("href", ""),
            'date_posted': date_posted,
        })
    return jobs


def scrape_tunisie_travail():
    # URL of the Tunisie Travail website
    url = "https://www.tunisietravail.net/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the page. Status code: {response.status_code}")
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all job postings (each job is inside a <div> with class "Post")
    job_cards = soup.find_all('div', class_='Post')

    # Extract job details
    jobs = []

    for job in job_cards:
        # Job Title (inside an <a> tag with class "h1titleall")
        title_tag = job.find('a', class_='h1titleall')
        date_tag = job.find('p', class_='PostDateIndexRed')
        description_tag = job.find(
            "div", style="line-height:18px;font-size:12px; font-family:Verdana, Geneva, sans-serif")
        title = title_tag.text.strip() if title_tag else "No title"
        description = description_tag.text.strip() if description_tag else "No description"
        date = date_tag.text.strip() if date_tag else None
        job_url = title_tag['href']
        company = title.split(" recrute ")[
            0] if " recrute " in title else "No company"

        # Logo URL (inside an <img> tag)
        logo_tag = job.find('img')
        logo_url = logo_tag['src'] if logo_tag else "No logo found"
        if "data:" in logo_url:
            logo_url = logo_tag["data-lazy-src"]
        # Append to the list
        jobs.append({
            'title': title,
            'description': description,
            'company': company,
            'location': None,
            'source_logo': logo_url,
            'source_website': "Tunisie Travail",
            'job_url': title_tag.get("href", ""),
            'date_posted': date,
        })
    return jobs


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
