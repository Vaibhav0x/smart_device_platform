from django.contrib import admin
from .models import User, Device, DeviceLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "role", "is_active", "is_staff")
    search_fields = ("email", "name")

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "status", "owner", "last_active_at")
    list_filter = ("type", "status")
    search_fields = ("name", "id")

@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "event", "value", "timestamp")
    list_filter = ("event",)
    search_fields = ("device__name", "event")