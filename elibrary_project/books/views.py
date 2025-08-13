from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
import os
import fitz  # PyMuPDF
from PIL import Image
from .models import Book, BookPage, Favorite
from .forms import BookForm, BookEditForm, SearchForm
from .utils import analyze_book_text

@login_required
def catalog_view(request):
    books = Book.objects.all().order_by('-created_at')
    
    # Filter by favorites
    show_favorites = request.GET.get('favorites', '0')
    if show_favorites == '1':
        favorite_books = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)
        books = books.filter(id__in=favorite_books)
    
    # Filter by genre
    genre = request.GET.get('genre')
    if genre:
        books = books.filter(genre=genre)
    
    # Search functionality
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(year__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user's favorite books for template
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'show_favorites': show_favorites,
        'selected_genre': genre,
        'user_favorites': user_favorites,
        'genres': Book.GENRE_CHOICES,
    }
    return render(request, 'books/catalog.html', context)

@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    
    context = {
        'book': book,
        'is_favorite': is_favorite,
    }
    return render(request, 'books/detail.html', context)

@login_required
def upload_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            
            # Process PDF to images
            try:
                process_pdf_to_images(book)
                messages.success(request, 'Buku berhasil diupload!')
                return redirect('books:detail', pk=book.pk)
            except Exception as e:
                book.delete()
                messages.error(request, f'Gagal memproses PDF: {str(e)}')
    else:
        form = BookForm()
    
    return render(request, 'books/upload.html', {'form': form})

def process_pdf_to_images(book):
    """Convert PDF pages to images using PyMuPDF"""
    pdf_path = book.pdf_file.path
    
    # Open PDF
    pdf_document = fitz.open(pdf_path)
    
    # Create directory for pages if it doesn't exist
    pages_dir = os.path.join(os.path.dirname(pdf_path), 'pages')
    os.makedirs(pages_dir, exist_ok=True)
    
    # Convert each page to image
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Render page as image
        mat = fitz.Matrix(1.5, 1.5)  # Scaling factor
        pix = page.get_pixmap(matrix=mat)
        
        # Save as PNG
        image_filename = f'page_{page_num + 1}.png'
        image_path = os.path.join(pages_dir, image_filename)
        pix.save(image_path)
        
        # Create BookPage object
        BookPage.objects.create(
            book=book,
            page_number=page_num + 1,
            image=f'books/pages/{book.id}/{image_filename}'
        )
    
    # Update total pages
    book.total_pages = len(pdf_document)
    
    # Create cover from first page if no cover exists
    if not book.cover and len(pdf_document) > 0:
        first_page = pdf_document.load_page(0)
        mat = fitz.Matrix(0.5, 0.5)  # Smaller for cover
        pix = first_page.get_pixmap(matrix=mat)
        cover_path = os.path.join(os.path.dirname(pdf_path), 'cover.png')
        pix.save(cover_path)
        book.cover = f'books/covers/{book.id}/cover.png'
    
    book.save()
    pdf_document.close()

@login_required
def edit_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # If new PDF file is uploaded, reprocess it
            if 'pdf_file' in request.FILES:
                # Delete old pages
                book.bookpage_set.all().delete()
                
                # Process new PDF
                book = form.save()
                try:
                    process_pdf_to_images(book)
                    messages.success(request, 'Buku berhasil diperbarui!')
                except Exception as e:
                    messages.error(request, f'Gagal memproses PDF: {str(e)}')
            else:
                form.save()
                messages.success(request, 'Buku berhasil diperbarui!')
            
            return redirect('books:detail', pk=book.pk)
    else:
        form = BookEditForm(instance=book)
    
    return render(request, 'books/edit.html', {'form': form, 'book': book})

@login_required
def delete_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Buku berhasil dihapus!')
        return redirect('books:catalog')
    
    return render(request, 'books/delete.html', {'book': book})

@login_required
def preview_book_view(request, pk, page_num=1):
    book = get_object_or_404(Book, pk=pk)
    
    # Get specific page
    try:
        page = BookPage.objects.get(book=book, page_number=page_num)
    except BookPage.DoesNotExist:
        raise Http404("Halaman tidak ditemukan")
    
    # Check if previous/next pages exist
    has_previous = BookPage.objects.filter(book=book, page_number=page_num-1).exists()
    has_next = BookPage.objects.filter(book=book, page_number=page_num+1).exists()
    
    context = {
        'book': book,
        'page': page,
        'current_page': page_num,
        'has_previous': has_previous,
        'has_next': has_next,
    }
    return render(request, 'books/preview.html', context)

@login_required
@require_POST
def toggle_favorite_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def analyze_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            # Extract text from PDF and analyze
            keywords = analyze_book_text(book.pdf_file.path)
            book.keywords = ', '.join(keywords[:20])  # Store top 20 keywords
            book.save()
            
            messages.success(request, 'Analisis buku berhasil!')
        except Exception as e:
            messages.error(request, f'Gagal menganalisis buku: {str(e)}')
        
        return redirect('books:detail', pk=book.pk)
    
    return render(request, 'books/analyze.html', {'book': book})
