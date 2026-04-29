from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import BookCard, Genre, Author, CoverType, City
User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    """Краткая информация об авторе объявления"""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'avatar',
        )

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'genre_name',
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'author_name',
        )


class CoverTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverType
        fields = (
            'id',
            'name',
        )

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'city',
        )



class BookCardSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    user = UserShortSerializer(read_only=True)
    cover_type = CoverTypeSerializer(read_only=True)

    class Meta:
        model = BookCard
        fields = (
            'id',
            'book_title',
            'pages_count',
            'photo',
            'is_active',
            'genre',
            'author',
            'cover_type',
            'user',
            'city',
            'created_at',
        )

class BookCardCreateSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(write_only=True)
    genre_name = serializers.CharField(write_only=True)
    city_name = serializers.CharField(write_only=True)
    cover_type_name = serializers.CharField(write_only=True)

    class Meta:
        model = BookCard
        fields = (
            'id',
            'book_title',
            'pages_count',
            'photo',
            'author_name',
            'genre_name',
            'city_name',
            'cover_type_name',
        )

    def get_or_create_by_name(self, model, field_name, value):
        value = value.strip()

        existing_object = model.objects.filter(
            **{f'{field_name}__iexact': value}
        ).first()

        if existing_object:
            return existing_object

        return model.objects.create(**{field_name: value})

    def create(self, validated_data):
        author_name = validated_data.pop('author_name')
        genre_name = validated_data.pop('genre_name')
        city_name = validated_data.pop('city_name')
        cover_type_name = validated_data.pop('cover_type_name')

        author = self.get_or_create_by_name(
            Author,
            'author_name',
            author_name
        )

        genre = self.get_or_create_by_name(
            Genre,
            'genre_name',
            genre_name
        )

        city = self.get_or_create_by_name(
            City,
            'city',
            city_name
        )

        cover_type = self.get_or_create_by_name(
            CoverType,
            'name',
            cover_type_name
        )

        book_card = BookCard.objects.create(
            author=author,
            genre=genre,
            city=city,
            cover_type=cover_type,
            **validated_data
        )

        return book_card
    
class BookCardUpdateSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(write_only=True, required=False)
    genre_name = serializers.CharField(write_only=True, required=False)
    city_name = serializers.CharField(write_only=True, required=False)
    cover_type_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = BookCard
        fields = (
            'id',
            'book_title',
            'pages_count',
            'photo',
            'author_name',
            'genre_name',
            'city_name',
            'cover_type_name',
        )

    def get_or_create_by_name(self, model, field_name, value):
        value = value.strip()

        existing_object = model.objects.filter(
            **{f'{field_name}__iexact': value}
        ).first()

        if existing_object:
            return existing_object

        return model.objects.create(**{field_name: value})

    def update(self, instance, validated_data):
        author_name = validated_data.pop('author_name', None)
        genre_name = validated_data.pop('genre_name', None)
        city_name = validated_data.pop('city_name', None)
        cover_type_name = validated_data.pop('cover_type_name', None)

        if author_name:
            instance.author = self.get_or_create_by_name(
                Author,
                'author_name',
                author_name
            )

        if genre_name:
            instance.genre = self.get_or_create_by_name(
                Genre,
                'genre_name',
                genre_name
            )

        if city_name:
            instance.city = self.get_or_create_by_name(
                City,
                'city',
                city_name
            )

        if cover_type_name:
            instance.cover_type = self.get_or_create_by_name(
                CoverType,
                'name',
                cover_type_name
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance