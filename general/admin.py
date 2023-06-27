from django.contrib import admin

from general.models import *


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'message']
    list_display_links = ['id', 'name']
    search_fields = list_display
    list_filter = ['created_at']
    fieldsets = (
        (
            None, 
            {
                "fields": ["name", "email", "phone", "message"],
            }
        ),
        (
            "Important Dates",
            {
                "fields": ["created_at", "updated_at"]
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rating', 'title']
    list_display_links = ['id', 'name']
    search_fields = list_display
    list_filter = ['created_at']
    fieldsets = (
        (
            None, 
            {
                "fields": ["name", "image", "rating", "title", "message"],
            }
        ),
        (
            "Important Dates",
            {
                "fields": ["created_at", "updated_at"]
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")
