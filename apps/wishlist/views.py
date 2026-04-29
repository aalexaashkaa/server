from django.db.models import Q
from rest_framework import generics, permissions

from apps.ads.models import BookCard
from apps.ads.serializers import BookCardSerializer

from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistItemListCreateView(generics.ListCreateAPIView):
    """Список желаний текущего пользователя и добавление новой книги"""

    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistItemDeleteView(generics.DestroyAPIView):
    """Удаление книги из списка желаний"""

    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


class WishlistMatchesView(generics.ListAPIView):
    """Объявления, которые совпадают со списком желаний пользователя"""

    serializer_class = BookCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wishlist_items = WishlistItem.objects.filter(user=self.request.user)

        query = Q()

        for item in wishlist_items:
            query |= Q(
                book_title__iexact=item.name,
                author__author_name__iexact=item.author
            )

        if not query:
            return BookCard.objects.none()

        return BookCard.objects.select_related(
            'genre',
            'author',
            'cover_type',
            'user',
            'city',
        ).filter(
            query,
            is_active=True
        ).exclude(
            user=self.request.user
        ).distinct()