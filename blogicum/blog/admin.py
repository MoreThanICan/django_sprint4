from django.contrib import admin
from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published', 'created_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published', 'created_at')
    ordering = ('name',)
    list_per_page = 50


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'location',
        'pub_date',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'category', 'location', 'pub_date')
    date_hierarchy = 'pub_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'post',
        'created_at',
    )
    search_fields = ('text',)
    list_filter = ('created_at',)
