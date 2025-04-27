from django.contrib import admin
from .models import Task
from .models import Order, CodeItem, Procedure, Tool, Component, Profile

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Order)
admin.site.register(CodeItem)
admin.site.register(Procedure)
admin.site.register(Tool)
admin.site.register(Component)
admin.site.register(Profile)