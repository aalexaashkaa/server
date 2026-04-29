from django.db import models
from django.conf import settings

class Genre(models.Model):
    """Модель жанров"""
    
    genre_name = models.CharField(max_length=255, unique=True)
	
    class Meta:
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        
    def __str__(self):
        return self.genre_name
    
class Author(models.Model):
    """Модель авторов"""
    
    author_name = models.CharField(max_length=255, unique=True)
	
    class Meta:
        db_table = 'authors'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        
    def __str__(self):
        return self.author_name
    
class City(models.Model):
    """Модель города"""
    
    city = models.CharField(max_length=255, unique=True)
	
    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        
    def __str__(self):
        return self.city
    

class CoverType(models.Model):
	"""Модель типа обложки"""

	name = models.CharField(max_length=100, unique=True)
      
	class Meta:
		db_table = 'cover_types'
		verbose_name = 'Cover type'
		verbose_name_plural = 'Cover types'

	def __str__(self):
		return self.name


class BookCard(models.Model):
	"""Карточка объявления книги"""


	book_title = models.CharField(max_length=255)
	pages_count = models.PositiveIntegerField()
	photo = models.ImageField(upload_to='book_cards/', blank=True, null=True)
	is_active = models.BooleanField(default=True)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='book_cards'
	)

	genre = models.ForeignKey(
		Genre,
		on_delete=models.PROTECT,
		related_name='book_cards'
	)

	author = models.ForeignKey(
		Author,
		on_delete=models.PROTECT,
		related_name='book_cards'
	)
      
	city = models.ForeignKey(
		City,
		on_delete=models.PROTECT,
		related_name='book_cards'
            
	)

	cover_type = models.ForeignKey(
		CoverType,
		on_delete=models.PROTECT,
		related_name='book_cards'
	)

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'book_cards'
		verbose_name = 'Book card'
		verbose_name_plural = 'Book cards'
		ordering = ['-created_at']

	def __str__(self):
		return self.book_title