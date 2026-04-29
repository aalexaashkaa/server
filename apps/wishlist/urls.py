from django.urls import path

from . import views

urlpatterns = [
    path('items/', views.WishlistItemListCreateView.as_view(), name='wishlist_items'),
    path('items/<int:pk>/', views.WishlistItemDeleteView.as_view(), name='wishlist_item_delete'),
    path('matches/', views.WishlistMatchesView.as_view(), name='wishlist_matches'),
]