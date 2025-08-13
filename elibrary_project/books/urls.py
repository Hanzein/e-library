from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('upload/', views.upload_book_view, name='upload'),
    path('<int:pk>/', views.book_detail_view, name='detail'),
    path('<int:pk>/edit/', views.edit_book_view, name='edit'),
    path('<int:pk>/delete/', views.delete_book_view, name='delete'),
    path('<int:pk>/preview/', views.preview_book_view, name='preview'),
    path('<int:pk>/preview/<int:page_num>/', views.preview_book_view, name='preview_page'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('<int:pk>/analyze/', views.analyze_book_view, name='analyze'),
]