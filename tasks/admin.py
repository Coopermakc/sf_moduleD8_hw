from django.contrib import admin

from tasks.models import TodoItem, Category, PriorityHigh, PriorityLow, PriorityMedium


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')

@admin.register(PriorityHigh)
class PriorityHighAdmin(admin.ModelAdmin):
    list_display= ['count']

@admin.register(PriorityMedium)
class PriorityMediumAdmin(admin.ModelAdmin):
    list_display= ['count']

@admin.register(PriorityLow)
class PriorityLowAdmin(admin.ModelAdmin):
    list_display= ['count']