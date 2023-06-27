from django.contrib import admin
from property.models import Property

# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=['pg_name','active','verified']
    list_filter=('created_at','active','verified','city','single_room','double_room','triple_room','four_room')
    search_fields=('user','pg_name')