from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from photologue.models import Gallery, Photo
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Категория товара"""
    name = models.CharField(unique=True, max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children')
    slug = models.SlugField(max_length=100, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель Товара"""
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    full_description = models.TextField('Полное описание')
    price = models.IntegerField('Цена', default=0)
    slug = models.SlugField(max_length=150)
    availability = models.BooleanField('Наличие', default=True)
    quantity = models.IntegerField('Количество', default=0)
    photo = models.OneToOneField(
        Photo,
        verbose_name='Главная фотография',
        on_delete=models.SET_NULL,
        null=True)
    gallery = models.ForeignKey(
        Gallery,
        verbose_name='Фотографии',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Cart(models.Model):
    """Корзина"""
    session = models.CharField('Сессия пользователя', max_length=500, null=True, blank=True)
    user = models.ForeignKey(
        User, verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True
    )
    accepted = models.BooleanField(verbose_name='Принято к заказу', default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return '{}'.format(self.user)


class CartItem(models.Model):
    """Товары в корзине"""
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price_sum = models.PositiveIntegerField('Общая сумма', default=0)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.price_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.cart)


class Order(models.Model):
    """Заказы"""
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name='Заказ выполнен', default=False)
    date = models.DateTimeField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    class MPTTMeta:
        order_insertion_by = ['date']

    def __str__(self):
        return '{}'.format(self.cart)


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Create user cart"""
    if created:
        Cart.objects.create(user=instance)
