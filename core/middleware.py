class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE') and request.user.is_authenticated:
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
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                path=request.path,
                method=request.method,
            )

        return response

    def _get_action(self, request):
        if request.method == 'DELETE':
            return 'Delete'
        elif request.method in ('PUT', 'PATCH'):
            return 'Update'
        elif request.method == 'POST':
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
        return ''

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
