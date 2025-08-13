from django.contrib import admin
from .models import Book, BookPage, Favorite

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'year', 'total_pages', 'created_at']
    list_filter = ['genre', 'year', 'created_at']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ['total_pages', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Buku', {
            'fields': ('title', 'author', 'description', 'year', 'genre')
        }),
        ('File', {
            'fields': ('pdf_file', 'cover')
        }),
        ('Analisis', {
            'fields': ('keywords',)
        }),
        ('Metadata', {
            'fields': ('total_pages', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(BookPage)
class BookPageAdmin(admin.ModelAdmin):
    list_display = ['book', 'page_number']
    list_filter = ['book']
    search_fields = ['book__title']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'book__title']