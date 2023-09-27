from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
	list_display = ['day', 'date']
	list_display_links = ['day']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['category']
	list_display_links = ['category']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'name', 'created_at', 'updated_at']
	list_display_links = ['id']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ['id', 'event', 'image', 'created_at', 'updated_at']
	list_display_links = ['id']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ['id', 'event', 'menu', 'price', 'is_soldout', 'created_at', 'updated_at']
	list_display_links = ['id']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'event', 'content', 'created_at', 'updated_at']
	list_display_links = ['id']
	
@admin.register(Notice)
class EventNoticeAdmin(admin.ModelAdmin):
	list_display = ['id', 'content', 'event']
	list_display_links = ['id']