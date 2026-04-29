from django.conf import settings
from django.db import models


class WishlistItem(models.Model):
    """Желаемая книга пользователя"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )

    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlist_items'
        verbose_name = 'Wishlist item'
        verbose_name_plural = 'Wishlist items'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} — {self.name}'