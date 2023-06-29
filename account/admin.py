from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import Response, Subscription, User


# Register your models here.
admin.site.register(Subscription)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'discounted_price', 'responses', 'verified_tag')

    def has_change_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        return False


class UserAdmin(BaseUserAdmin):
    list_display = ['id', "email", "name", "phone_number", "is_staff", "is_subscribed"]
    list_display_links = ['id', "email"]
    
    list_filter=('date_joined',)
    ordering=['-date_joined']
    

    fieldsets = (
        (None, {
            "fields": ("email", "password", "username"),
        }),
        ("Personal Information", {
            "fields": ("name", "phone_number", "subscription", "responses", "is_subscribed"),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        })
    )
    readonly_fields = ['date_joined', 'last_login', 'username']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)

    def get_fieldsets(self, request, obj= None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets
        return [f for f in fieldsets if f[0] != 'Permissions']


admin.site.register(User, UserAdmin)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("name", "email", "phone", "property"),
        }),
        ('Important Dates', {
            'fields': ('date', 'time'),
        })
    )
    readonly_fields = ['date', 'time']





