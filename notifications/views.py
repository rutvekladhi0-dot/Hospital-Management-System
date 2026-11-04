from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils.timesince import timesince
from .models import Notification


@login_required
def notification_list_view(request):
    queryset = Notification.objects.filter(recipient=request.user).select_related('sender')

    context = {
        'notifications': queryset,
        'table_id': 'notificationTable',
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
def notification_api_view(request):
    notifications = Notification.objects.filter(recipient=request.user).select_related('sender')[:10]
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()

    data = []
    for n in notifications:
        data.append({
            'id': n.pk,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'badge_class': n.type_badge_class,
            'is_read': n.is_read,
            'link': n.link or '#',
            'time_ago': timesince(n.created_at) + ' ago',
        })

    return JsonResponse({'notifications': data, 'unread_count': unread_count})


@login_required
@require_POST
def notification_mark_read_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'ok', 'message': 'Notification marked as read.'})


@login_required
@require_POST
def notification_mark_all_read_view(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok', 'message': 'All notifications marked as read.'})


@login_required
@require_POST
def notification_delete_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.delete()
    return JsonResponse({'status': 'ok', 'message': 'Notification deleted.'})
