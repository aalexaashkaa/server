from django.urls import path

from . import views


urlpatterns = [
    path('book-cards/', views.BookCardListView.as_view(), name='book_cards'),
    path('my-book-cards/', views.MyBookCardListView.as_view(), name='my_book_cards'),
    path('book-cards/<int:pk>/', views.BookCardDetailView.as_view(), name='book_card_detail'),
    path('book-cards/create/', views.BookCardCreateView.as_view(), name='book_card_create'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('cities/', views.CityListView.as_view(), name='cities'),
    
]