# 📚 Django E-Library

Sistem **E-Library** berbasis Django dengan fitur katalog buku, preview PDF, manajemen profil pengguna, dan analisis kata kunci.

---

## 🚀 Langkah 1: Persiapan Environment

```bash
# Aktivasi virtual environment (jika belum)
source elibrary_env/bin/activate  # Linux/macOS
# atau
elibrary_env\Scripts\activate     # Windows

# Install semua dependencies
pip install -r requirements.txt
```
## 🗄️ Langkah 2: Setup Database PostgreSQL

Install PostgreSQL di sistem Anda.
Buat database dan user:
```bash
-- Masuk ke PostgreSQL sebagai superuser
sudo -u postgres psql

-- Buat database dan user
CREATE DATABASE elibrary_db;
CREATE USER elibrary_user WITH PASSWORD 'password123';
ALTER ROLE elibrary_user SET client_encoding TO 'utf8';
ALTER ROLE elibrary_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE elibrary_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE elibrary_db TO elibrary_user;
\q
```

## ⚙️ Langkah 3: Konfigurasi Django
```bash
# Masuk ke direktori project
cd elibrary_project

# Buat migrasi
python manage.py makemigrations accounts
python manage.py makemigrations books

# Apply migrasi
python manage.py migrate

# Buat superuser untuk admin
python manage.py createsuperuser
```

Buat direktori media:
```bash
mkdir -p media/books/pdfs
mkdir -p media/books/covers
mkdir -p media/books/pages
mkdir -p media/profiles
```
Download NLTK data:
```bash
python manage.py shell
Di dalam Python shell:
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
exit()
```

## 🎨 Langkah 4: Konfigurasi File Static
```bash
# Buat direktori static
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Collect static files
python manage.py collectstatic
```

## ▶️ Langkah 5: Jalankan Server
```bash
python manage.py runserver
```
Aplikasi akan berjalan di: http://127.0.0.1:8000/

## ✨ Fitur yang Sudah Diimplementasi
- ✅ Login dengan email dan password  
- ✅ Registrasi dengan validasi password  
- ✅ Top navbar dengan menu lengkap  
- ✅ Katalog buku dengan ListView dan pagination  
- ✅ Filter favorit dan genre  
- ✅ Pencarian berdasarkan judul, tahun, deskripsi  
- ✅ Detail buku dengan semua informasi  
- ✅ Preview buku dengan navigasi halaman  
- ✅ Upload buku dengan konversi PDF ke gambar  
- ✅ Edit buku  
- ✅ Hapus buku dengan konfirmasi  
- ✅ Toggle favorit  
- ✅ Profil user dengan foto  
- ✅ Edit profil  
- ✅ Ubah password  
- ✅ Analisis buku untuk kata kunci  
- ✅ Responsive design dengan Bootstrap 5  
