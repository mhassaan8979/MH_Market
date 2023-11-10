from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.

class Slider(models.Model):

    DEAL = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arraivels','New Arraivels'),
        ('New DEALS','New DEALS'),
    )

    image = models.ImageField(upload_to='slider_image')
    deal = models.CharField(choices=DEAL, max_length=100)
    sale = models.IntegerField()
    brand = models.CharField(max_length=200)
    discount = models.IntegerField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.brand


class Banner(models.Model):
    image = models.ImageField(upload_to='banner_image')
    deal = models.CharField(max_length=200)
    feature = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)
     
    def __str__(self):
        return self.feature
    

class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " -- " + self.main_category.name
    

class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name
    

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    quantity = models.IntegerField()
    availability = models.IntegerField()
    image = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField()
    product_info = RichTextField()
    model_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=100)


class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)


CITY_CHOICES = (
    ('Lahore', 'Lahore'),
    ('Karachi', 'Karachi'),
    ('Islamabad', 'Islamabad'),
    ('Fasilabad', 'Fasilabad'),
    ('Peshawar', 'Peshawar'),
    ('Sailkot', 'Sailkot'),
    ('Rawalpindi', 'Rawalpindi'),
    ('Qouta', 'Qouta'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(choices=CITY_CHOICES, max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.id)

