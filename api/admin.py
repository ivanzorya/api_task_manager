from django.contrib import admin

from .models import Task, Change


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created', 'completed')
    search_fields = ('title',)
    list_filter = ('status',)


class ChangeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'task', 'field_name', 'pub_date')
    search_fields = ('field_name',)
    list_filter = ('task',)


admin.site.register(Change, ChangeAdmin)
admin.site.register(Task, TaskAdmin)
