from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import User, Role


class RoleInline(admin.TabularInline):
    model = User.roles.through
    extra = 1
    verbose_name = _('role')
    verbose_name_plural = _('roles')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone',
                    'gender', 'image_tag', 'is_verified', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_verified', 'gender', 'roles')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['export_as_csv']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone',
                       'gender', 'date_of_birth', 'address', 'profile_picture')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified',
                       'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone',
                       'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    inlines = [RoleInline]

    def image_tag(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;" />', obj.profile_picture.url)
        return '-'
    image_tag.short_description = 'Photo'

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Phone', 'Gender', 'Roles', 'Active'])
        for user in queryset:
            roles = ', '.join(user.roles.values_list('name', flat=True))
            writer.writerow([user.username, user.email, user.first_name, user.last_name, user.phone, user.gender, roles, user.is_active])
        return response
    export_as_csv.short_description = "Export selected users as CSV"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
