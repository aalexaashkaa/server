from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import BookCard, Genre, Author, City, CoverType
from .serializers import (
    BookCardSerializer,
    GenreSerializer,
    AuthorSerializer,
    CoverTypeSerializer,
    CitySerializer,
    BookCardCreateSerializer,
    BookCardUpdateSerializer
)


class BookCardListView(generics.ListAPIView):
    """Список объявлений с фильтрами"""

    serializer_class = BookCardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = BookCard.objects.select_related(
            'genre',
            'author',
            'cover_type',
            'user',
            'city',
        ).all()

        genre = self.request.query_params.get('genre')
        author = self.request.query_params.get('author')
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')
        city = self.request.query_params.get('city')

        if genre:
            queryset = queryset.filter(genre_id=genre)

        if author:
            queryset = queryset.filter(author_id=author)


        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)

            if is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)

        if search:
            queryset = queryset.filter(book_title__icontains=search)

        if city:
            queryset = queryset.filter(city_id=city)

        return queryset


class GenreListView(generics.ListAPIView):
    """Список жанров для фильтра"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


class AuthorListView(generics.ListAPIView):
    """Список авторов для фильтра"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CoverTypeListView(generics.ListAPIView):
    """Список типов обложки"""

    queryset = CoverType.objects.all()
    serializer_class = CoverTypeSerializer
    permission_classes = [permissions.AllowAny]
class CityListView(generics.ListAPIView):
    """Список городов для фильтра"""

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

class MyBookCardListView(generics.ListAPIView):
    """Список объявлений текущего пользователя"""

    serializer_class = BookCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookCard.objects.select_related(
            'genre',
            'author',
            'cover_type',
            'user',
            'city',
        ).filter(user=self.request.user)
    
class BookCardCreateView(generics.CreateAPIView):
    """Создание объявления"""

    serializer_class = BookCardCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование и удаление объявления"""

    serializer_class = BookCardUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return BookCard.objects.filter(user=self.request.user)