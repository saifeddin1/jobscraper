from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Notification
from django.db.models import Q
from django.shortcuts import get_object_or_404

@login_required
def get_notifications(request):
    """
    Fetch paginated notifications for the logged-in user.
    """
    page = int(request.GET.get("page", 1))  # Default to first page
    per_page = 5  # Adjust the number of notifications per page

    notifications = Notification.objects.filter(Q(user=request.user) | Q(notification_type="new_jobs_added")).order_by("-created_at")
    unread_count = notifications.filter(is_read=False).count()

    # Paginate notifications
    paginator = Paginator(notifications, per_page)
    current_page = paginator.get_page(page)

    data = [
        {
            "id": n.id,
            "type": n.notification_type,
            "message": n.message,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read": n.is_read,
        }
        for n in current_page
    ]

    return JsonResponse({
        "notifications": data,
        "unread_count": unread_count,
        "has_next": current_page.has_next(),  # Whether there's another page
        "next_page": page + 1 if current_page.has_next() else None
    })

@login_required
def mark_notification_as_read(request, notification_id):
    """
    Mark a specific notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})