from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Exchange
from .serializers import (
	ExchangeCreateSerializer,
	ExchangeSerializer,
	ExchangeStatusUpdateSerializer,
)


class ExchangeCreateView(generics.CreateAPIView):
	"""Создание заявки на обмен"""

	serializer_class = ExchangeCreateSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		book_card = serializer.validated_data['book_card']

		serializer.save(
			initiator=self.request.user,
			receiver=book_card.user
		)


class MyExchangeListView(generics.ListAPIView):
	"""Список обменов текущего пользователя"""

	serializer_class = ExchangeSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Exchange.objects.select_related(
			'initiator',
			'receiver',
			'book_card',
			'book_card__author',
			'book_card__genre',
			'book_card__city',
			'book_card__cover_type',
			'book_card__user',
		).filter(
			Q(initiator=self.request.user) | Q(receiver=self.request.user)
		)


class ExchangeStatusUpdateView(generics.UpdateAPIView):
	"""Принять или отклонить обмен"""

	serializer_class = ExchangeStatusUpdateSerializer
	permission_classes = [permissions.IsAuthenticated]
	http_method_names = ['patch']

	def get_queryset(self):
		return Exchange.objects.all()

	def perform_update(self, serializer):
		exchange = self.get_object()

		if exchange.receiver != self.request.user:
			raise PermissionDenied(
				'Только получатель предложения может принять или отклонить обмен.'
			)

		serializer.save()