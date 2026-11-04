import logging

logger = logging.getLogger(__name__)


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.method in ('POST', 'PUT', 'PATCH', 'DELETE')
            and getattr(request, 'user', None)
            and request.user.is_authenticated
        ):
            try:
                from auditlogs.models import AuditLog

                action = self._get_action(request)
                model_name = self._get_model_name(request)
                object_id = self._get_object_id(request)

                AuditLog.objects.create(
                    user=request.user,
                    action=action,
                    model_name=model_name,
                    object_id=object_id,
                    description=f'{action} on {model_name} (ID: {object_id})' if object_id else f'{action} on {model_name}',
                    ip_address=self._get_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    path=request.path[:500],
                    method=request.method,
                )
            except Exception as e:
                logger.warning('AuditLogMiddleware failed to record log: %s', e)

        return response

    def _get_action(self, request):
        if request.method == 'DELETE':
            return 'Delete'
        elif request.method in ('PUT', 'PATCH'):
            return 'Update'
        elif request.method == 'POST':
            if request.path.endswith('/login/'):
                return 'Login'
            return 'Create'
        return 'View'

    def _get_model_name(self, request):
        parts = [p for p in request.path.strip('/').split('/') if p]
        if parts:
            return parts[-1] if parts[-1] not in ('create', 'update', 'delete', 'list') else parts[-2] if len(parts) > 1 else 'unknown'
        return 'unknown'

    def _get_object_id(self, request):
        parts = request.path.strip('/').split('/')
        for part in parts:
            if part.isdigit():
                return part
        return None

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        if not ip:
            return None

        # Strip port from IPv4 if present (e.g. 1.2.3.4:5678)
        if ':' in ip and '.' in ip:
            ip = ip.split(':')[0]

        try:
            from django.core.validators import validate_ipv46_address
            validate_ipv46_address(ip)
            return ip
        except Exception:
            return None
