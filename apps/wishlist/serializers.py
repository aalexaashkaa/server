from rest_framework import serializers

from .models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = (
            'id',
            'author',
            'name',
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )

    def validate(self, attrs):
        request = self.context.get('request')

        author = attrs.get('author', '').strip()
        name = attrs.get('name', '').strip()

        if not author:
            raise serializers.ValidationError({
                'author': 'Введите автора.'
            })

        if not name:
            raise serializers.ValidationError({
                'name': 'Введите название книги.'
            })

        if request and request.user.is_authenticated:
            exists = WishlistItem.objects.filter(
                user=request.user,
                author__iexact=author,
                name__iexact=name
            ).exists()

            if exists:
                raise serializers.ValidationError(
                    'Эта книга уже есть в списке желаний.'
                )

        attrs['author'] = author
        attrs['name'] = name

        return attrs