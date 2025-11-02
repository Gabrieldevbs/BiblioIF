from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class InfoUser(models.Model):
    USER_TYPES = [('admin', 'Administrador da Página'), ('common user', 'Usuário Comum')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/photos/', blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=50,default='common user')


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    pages = models.PositiveIntegerField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='books/photos/', blank=True, null=True)

class Category(models.Model):
    book = models.ManyToManyField(Book, related_name='categories')
    name = models.CharField(max_length=30)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='purchases')
    date_purchase = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f'O usuário {self.user.username} comprou o livro {self.book.title}!' 
      
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorites_by')
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return f'O usuário {self.user.username} favoritou o livro {self.book.title}!' 
