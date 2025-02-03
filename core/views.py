from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator   
 
from notifications.utils import create_notification
from .models import Job  
from collections import Counter 

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # scrape_all_jobs()

    jobs_list = Job.objects.all().order_by("-scraped_at") 
     
    # Pagination: Show 10 jobs per page
    paginator = Paginator(jobs_list, 12) 
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)

    print('user.favorited_jobs.add: ', request.user.favorited_jobs.all())
    return render(request, "scraper/job_list.html", {"jobs": jobs, "user":request.user})



@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "scraper/job_details.html", {"job": job})

 

@login_required
def dashboard_view(request):
    total_jobs = Job.objects.count()
    saved_jobs = request.user.favorited_jobs.count()

    # Count jobs by source website
    job_sources = Job.objects.values_list("source_website", flat=True)
    source_counts = dict(Counter(job_sources))

    # Count top 5 companies hiring
    job_companies = Job.objects.exclude(company__isnull=True).exclude(company="").values_list("company", flat=True)
    top_companies = dict(Counter(job_companies).most_common(5))  # Get the 5 most common companies

    # Count jobs per location
    job_locations = Job.objects.exclude(location__isnull=True).exclude(location="").values_list("location", flat=True)
    location_counts = dict(Counter(job_locations))

    # Convert data for JavaScript
    chart_data = {
        "sources": list(source_counts.keys()),
        "source_counts": list(source_counts.values()),
        "companies": list(top_companies.keys()),
        "company_counts": list(top_companies.values()),
        "locations": list(location_counts.keys()),
        "location_counts": list(location_counts.values()),
    }

    return render(
        request,
        "scraper/dashboard.html",
        {
            "jobs": total_jobs,
            "saved": saved_jobs,
            "chart_data": chart_data,
            "job_list": Job.objects.filter(location__isnull=False, company__isnull=False).order_by("-id")[:10],  # Last 10 jobs
        },
    )


@login_required
def saved_jobs_view(request): 
    user_jobs = request.user.favorited_jobs.all()
    return render(request, 'scraper/saved_jobs.html', 
                  {'user': request.user, "jobs":user_jobs,})


@login_required
def toggle_favorite(request, job_id):
    user = request.user
    job = get_object_or_404(Job, id=job_id)

    print("Logged in user:", user)  # Debugging

    if job in user.favorited_jobs.all():
        print(f"Removing {job} from {user}'s favorites")
        user.favorited_jobs.remove(job)  
        create_notification("job_unsaved", user, data={"job_title": job.title})

    else:
        print(f"Adding {job} to {user}'s favorites")
        user.favorited_jobs.add(job)   
        create_notification("job_saved", user, data={"job_title": job.title})


    user.save()  # This might be redundant, but no harm in keeping it

    print("Current favorited jobs:", user.favorited_jobs.all())  # Debugging
    return JsonResponse({"success": True})

 