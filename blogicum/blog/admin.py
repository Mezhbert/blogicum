from django.contrib import admin
from .models import Category, Post, Location, Comment

admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'is_published',
        'created_at',
        'slug'
    )
    list_editable = (
        'description',
        'is_published',
        'slug'
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'pub_date',
        'is_published',
        'location',
        'created_at',
    )
    list_editable = (
        'text',
        'author',
        'pub_date',
        'is_published',
        'location',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'created_at',
    )
    search_fields = ('text', 'author__username')
    list_display_links = ('text',)
