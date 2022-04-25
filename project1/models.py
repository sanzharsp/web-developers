from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
import pytz
import datetime
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
today = datetime.datetime.today()
Astana=today.astimezone(pytz.timezone('Asia/Almaty'))
DATA_TIME_FORMAT="%Y-%m-%d %H:%M:%S"
str_Astana_time=Astana.strftime(DATA_TIME_FORMAT)

User = get_user_model()
# Модель клиента
class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    is_verificate=models.BooleanField(verbose_name='Почта потверждена',default=False)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    create_customer=models.DateTimeField(verbose_name='Дата регистраций',auto_now_add=True)
    birth_date =models.DateTimeField(auto_now_add=True, verbose_name="Дата регистраций клиента")
    orders = models.ManyToManyField('Order',blank=True, verbose_name='Заказы покупателя', related_name='related_order')
    def __str__(self):
        return "Клиент: {} {}".format(self.user.first_name, self.user.last_name)
    class Meta:
        ordering = ['-birth_date']
        verbose_name='Клиенты'
        verbose_name_plural='Клиенты'


#Заказы клиента 


class Category(models.Model):

    name=models.CharField(max_length=50,verbose_name="Имя категории")
    slug=models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    birth_date = models.DateTimeField(auto_now_add=True,verbose_name="Дата добавления категории")


    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-birth_date']
        verbose_name='Категорий'
        verbose_name_plural='Категорий'


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

#подкатигория
class subcategories(models.Model):

    subcategories_slug = models.SlugField(unique=True)
    subcategory=models.CharField(max_length=255,verbose_name='подкатегория')
    birth_date =models.DateTimeField(auto_now_add=True,verbose_name="Дата добавления подкатегории")
    category_product=models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-birth_date']
        verbose_name='Подкатегорий'
        verbose_name_plural='Подкатегорий'
    def __str__(self):
        return self.subcategory

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)  


#Продукт
class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    subcategor=models.ForeignKey(subcategories,verbose_name='Подкатегория',on_delete=models.CASCADE,related_name='category')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Главная изображение товара')
    images_2=models.ImageField(verbose_name='Дочерние изображения',blank=True, null=True)
    images_3=models.ImageField(verbose_name='Дочерние изображения',blank=True,null=True)
    description = RichTextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Новая цена')
    count_product=models.DecimalField(max_digits=7,decimal_places=0,verbose_name="Количество товара",default=1)
    history_price=models.DecimalField(max_digits=9,decimal_places=0,verbose_name='Старая цена')
    birth_date =models.DateTimeField(auto_now_add=True,  verbose_name="Дата добавления")
    old_discount=models.DecimalField(max_digits=9,decimal_places=0,verbose_name='Цена до скидки',default=0)
    discount=models.DecimalField(max_digits=2,decimal_places=0,verbose_name="Скидка в процентах",default=0)
    discount_end_date =models.DateTimeField( verbose_name="Дата окончания скидки",default=datetime.datetime.strptime(str_Astana_time,DATA_TIME_FORMAT))
    value = models.CharField(choices=LIKE_CHOICES, max_length=8,default='Like')
    new = models.BooleanField(default=True,verbose_name="Новый продукт")
    likes = models.ManyToManyField(User,blank=True, related_name='likes')
    orders=models.DecimalField(max_digits=2000,decimal_places=0,verbose_name="Количество заказов",default=0)
    comments=GenericRelation('Comment')

    class Meta:
        ordering = ['-birth_date']
        verbose_name='Продукт'
        verbose_name_plural='Продукты'

    def __str__(self):
        return str(self.title)


    def clean_image(self):
        #рекомендуемое изображение 700x525
        super().save()
        img = Image.open(self.image)
        if (img.height!=270 or img.width!=270):
            width = 270
            height = 270
            resized_img = img.resize((width, height), Image.ANTIALIAS)
            resized_img.save(self.image.path)
        super().save()


    def clean(self):
    
          
        if  self.category_id and self.subcategor_id and self.category.name != self.subcategor.category_product.name:
            
            raise ValidationError('Категории у подкатегорий и продукта ({}!={}) не совподают \U0001F62A'.format(self.category.name,self.subcategor.category_product.name))


# Создание системы корзинаций 
class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1,verbose_name='Количество')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
  

    def __str__(self):
        return "{} Продукт для корзины {}".format(self.product.id,self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)
    class Meta:
        verbose_name='Продукты для корзины'
        verbose_name_plural='Продукты для корзины'


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-final_price']
        verbose_name='Корзина'
        verbose_name_plural='Корзина'



class Comment(models.Model):
    
    user=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Автор', on_delete=models.CASCADE)
    text=models.TextField(verbose_name='Текст Коментария')
    parent=models.ForeignKey(
        'self',
        verbose_name='Родительски коментарий',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE
    )
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    timestamp=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')
    is_child=models.BooleanField(default=False)
    

    def __str__(self):
        return "Коментарий "+str(self.id)
        
    class Meta:
        ordering = ['-timestamp']
        verbose_name='Коментарий'
        verbose_name_plural='Коментарий'




class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон',default="+7(---)-- -- --")
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=datetime.datetime.strptime(str_Astana_time,DATA_TIME_FORMAT))

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-created_at']
        verbose_name='Заказы'
        verbose_name_plural='Заказы'

# Реклама


class New_Recomedation(models.Model):
    black_text=models.CharField(max_length=75,verbose_name="Черный текст")
    red_text=models.CharField(max_length=75,verbose_name="Красный текст")
    images=models.ImageField(verbose_name="Изображение нового продукта !! желательно 1920 на 800")
    birth_date = models.DateTimeField(verbose_name="Дата добовления",auto_now_add=True)
    class Meta:
        ordering = ['-birth_date']
        verbose_name='Банер 1'
        verbose_name_plural='Банер для реклам'
    def __str__(self):
        return "Рекламный банер"
    def clean(self):
        super().save()
        img = Image.open(self.images)
        if (img.height!=1920 or img.width!=800):
            width = 1920
            height = 800
            resized_img = img.resize((width, height), Image.ANTIALIAS)
            resized_img.save(self.images.path)


class REKLAMA(models.Model):
    products=models.ForeignKey(Product,verbose_name="продукт каторый рекламируют",on_delete=models.CASCADE)
    image=models.ImageField(verbose_name="Изображение 1171 на 300",null=True )
    text=models.TextField(verbose_name="Текст",null=True)

    class Meta:
        ordering=['-products']
        verbose_name='Реклама'
        verbose_name_plural='Реклама'
    def __str__(self):
        return "{} Реклама".format(self.id)
    def clean(self):
        super().save()
        img = Image.open(self.image)
        if (img.height!=1171 or img.width!=300):
            width = 1171
            height = 300
            resized_img = img.resize((width, height), Image.ANTIALIAS)
            resized_img.save(self.image.path)


#Рассылка news
class NEWS_MODEL(models.Model):
    email=models.EmailField()


