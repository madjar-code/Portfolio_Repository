from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date")
    search_fields = ("name", "description", "technologies")
    list_filter = ("start_date", "end_date")
