from django.conf import settings
from django.db import models

from apps.ads.models import BookCard


class Exchange(models.Model):
    """Модель обмена книгами"""

    class ExchangeType(models.TextChoices):
        BOOKCROSSING = 'bookcrossing', 'Точка буккросинга'
        DELIVERY = 'delivery', 'Доставка'

    class ExchangeStatus(models.TextChoices):
        PENDING = 'pending', 'Ожидает ответа'
        ACCEPTED = 'accepted', 'Принято'
        DECLINED = 'declined', 'Отклонено'

    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='initiated_exchanges'
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_exchanges'
    )

    book_card = models.ForeignKey(
        BookCard,
        on_delete=models.CASCADE,
        related_name='exchanges'
    )

    exchange_type = models.CharField(
        max_length=30,
        choices=ExchangeType.choices
    )

    bookcrossing_address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    delivery_address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    delivery_method = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
		max_length=20,
		choices=ExchangeStatus.choices,
		default=ExchangeStatus.PENDING
	)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exchanges'
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchanges'
        ordering = ['-created_at']

    def __str__(self):
        return f'Exchange #{self.id}'