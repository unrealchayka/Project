from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    '''Пользователь'''
    age = models.DateField('Дата рождений', blank=True, null=True)
    social_network = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='owner/', default='defaultuesr.jpg')

    def get_absolute_url(self):
        return reverse('owner', kwargs={'pk' : self.pk})
        
    def __str__(self):
        return f'{self.username}'


class Category(models.Model):
    '''Категории товаров'''
    title = models.CharField(max_length=255,verbose_name='Категория')
    slug = models.SlugField(max_length=100,unique=True)
    in_stock = models.BooleanField('На главную?', default=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural ='Категории'

    def __str__(self) -> str:
        return f'{self.title}'


class Tag(models.Model):
    '''Теги'''
    title = models.CharField(max_length=255,verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True)
    in_stock = models.BooleanField('На главную?', default=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return str(self.title)


class Brand(models.Model):
    '''Бренд'''
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)
    in_stock= models.BooleanField('На главную?', default=False)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return str(self.title)


class Product(models.Model):
    '''Товары'''
    title = models.CharField(max_length=255, verbose_name='Товар')
    description = models.TextField(max_length=1024, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория товара')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField('Скидка', blank=True, default=0,validators=[MaxValueValidator(100)])
    pub_date = models.DateField('Дата обновления', auto_now=True)
    create = models.DateField('Дата создания', auto_now_add=True)
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество товаров в наличии')
    image = models.ImageField(upload_to='product/%Y/%m/%d/', blank=True, verbose_name='Основное фото')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name='Бренд')
    slug = models.SlugField(max_length=255)
    in_stock= models.BooleanField('На главную?', default=False)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug' : self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural ='Товары'

    def __str__(self) -> str:
        return f'{self.title}'


class RatingStar(models.Model):
    '''Звезда рейтинга'''
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-value']


class Rating(models.Model):
    '''Рейтинг'''
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, default=None, related_name='rating')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда', default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'star=> {self.star}  product=> {self.product}  user=> {self.user}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Comment(models.Model):
    '''Коментарии'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name='Пользователь', related_name='user_comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                    verbose_name='Новость', null=True,
                    blank=True, related_name='user_comment')
    create = models.DateTimeField('Время добавления коментария', auto_now_add=True)
    text = models.TextField('Коментарий')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментраии'


class Cart(models.Model):
    '''Корзина'''
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='cart')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Твоар')
    create = models.DateTimeField(auto_now_add=True)  
    quantit = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
     )

    def __str__(self):
            return f'{self.user} {self.products}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural ='Корзины'


class Checkout(models.Model):
    '''Заказ'''
    CHOICE_PAYMENT = (
        ('Наличный расчeт', 'Наличный расчeт'),
        ('Оплата картой', 'Оплата картой'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    addreses = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    comment = models.TextField(max_length=1500, null=True, blank=True)
    payment = models.CharField(max_length=20, choices=CHOICE_PAYMENT)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.username} {self.addreses}'




    