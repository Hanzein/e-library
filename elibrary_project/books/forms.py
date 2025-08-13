from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'title', 'description', 'author', 'year', 'genre']
        widgets = {
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul Buku'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi buku...'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Penulis'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tahun Terbit'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('File harus berformat PDF.')
            if file.size > 50 * 1024 * 1024:  # 50MB
                raise forms.ValidationError('Ukuran file maksimal 50MB.')
        return file

class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'title', 'description', 'author', 'year']
        widgets = {
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul Buku'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi buku...'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Penulis'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tahun Terbit'
            })
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari judul, tahun, atau deskripsi...'
        })
    )