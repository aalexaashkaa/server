from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.ads.serializers import BookCardSerializer
from apps.ads.models import BookCard

from .models import Exchange


User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
			'avatar',
		)


class ExchangeCreateSerializer(serializers.ModelSerializer):
	book_card = serializers.PrimaryKeyRelatedField(
		queryset=BookCard.objects.select_related('user').all()
	)

	class Meta:
		model = Exchange
		fields = (
			'id',
			'book_card',
			'exchange_type',
			'bookcrossing_address',
			'delivery_address',
			'delivery_method',
			'created_at',
		)
		read_only_fields = (
			'id',
			'created_at',
		)

	def validate(self, attrs):
		request = self.context.get('request')
		book_card = attrs.get('book_card')
		exchange_type = attrs.get('exchange_type')

		if request and book_card.user == request.user:
			raise serializers.ValidationError(
				'Нельзя оформить обмен со своим объявлением.'
			)

		if exchange_type == Exchange.ExchangeType.BOOKCROSSING:
			if not attrs.get('bookcrossing_address'):
				raise serializers.ValidationError({
					'bookcrossing_address': 'Укажите адрес точки буккросинга.'
				})

			attrs['delivery_address'] = None
			attrs['delivery_method'] = None

		elif exchange_type == Exchange.ExchangeType.DELIVERY:
			if not attrs.get('delivery_address'):
				raise serializers.ValidationError({
					'delivery_address': 'Укажите адрес доставки.'
				})

			if not attrs.get('delivery_method'):
				raise serializers.ValidationError({
					'delivery_method': 'Укажите способ доставки.'
				})

			attrs['bookcrossing_address'] = None

		return attrs


class ExchangeSerializer(serializers.ModelSerializer):
	initiator = UserShortSerializer(read_only=True)
	receiver = UserShortSerializer(read_only=True)
	book_card = BookCardSerializer(read_only=True)

	class Meta:
		model = Exchange
		fields = (
			'id',
			'initiator',
			'receiver',
			'book_card',
			'exchange_type',
			'bookcrossing_address',
			'delivery_address',
			'delivery_method',
			'status',
			'created_at',
		)


class ExchangeStatusUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Exchange
		fields = (
			'status',
		)

	def validate_status(self, value):
		if value not in [
			Exchange.ExchangeStatus.ACCEPTED,
			Exchange.ExchangeStatus.DECLINED,
		]:
			raise serializers.ValidationError(
				'Можно только принять или отклонить обмен.'
			)

		return value