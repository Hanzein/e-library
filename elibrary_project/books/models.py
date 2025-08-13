from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os

def book_pdf_path(instance, filename):
    return f'books/pdfs/{instance.id}/{filename}'

def book_cover_path(instance, filename):
    return f'books/covers/{instance.id}/{filename}'

def book_pages_path(instance, filename):
    return f'books/pages/{instance.book.id}/{filename}'

class Book(models.Model):
    GENRE_CHOICES = [
        ('fiksi', 'Fiksi'),
        ('komik', 'Komik'),
        ('motivasi', 'Motivasi'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    pdf_file = models.FileField(upload_to=book_pdf_path)
    cover = models.ImageField(upload_to=book_cover_path, null=True, blank=True)
    total_pages = models.PositiveIntegerField(default=0)
    keywords = models.TextField(blank=True, help_text="Kata kunci hasil analisis")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})
    
    def delete(self, *args, **kwargs):
        # Delete all related files
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):
                os.remove(self.pdf_file.path)
        
        if self.cover:
            if os.path.isfile(self.cover.path):
                os.remove(self.cover.path)
        
        # Delete all page images
        pages = self.bookpage_set.all()
        for page in pages:
            if page.image and os.path.isfile(page.image.path):
                os.remove(page.image.path)
        
        super().delete(*args, **kwargs)

class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField()
    image = models.ImageField(upload_to=book_pages_path)
    
    class Meta:
        unique_together = ['book', 'page_number']
        ordering = ['page_number']
    
    def __str__(self):
        return f"{self.book.title} - Page {self.page_number}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"