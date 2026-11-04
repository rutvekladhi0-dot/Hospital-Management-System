from django.conf import settings


def global_context(request):
    context = {
        'hospital_name': getattr(settings, 'HOSPITAL_NAME', 'Hospital'),
        'hospital_tagline': getattr(settings, 'HOSPITAL_TAGLINE', ''),
        'user_roles': [],
        'unread_notifications': 0,
    }

    if request.user.is_authenticated:
        context['user_roles'] = list(request.user.roles.values_list('name', flat=True))

        try:
            from notifications.models import Notification
            context['unread_notifications'] = Notification.objects.filter(
                recipient=request.user,
                is_read=False,
            ).count()
        except Exception:
            pass

    return context
