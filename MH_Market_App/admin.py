from django.contrib import admin
from .models import *

# Register your models here.

"""@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['id','image','deal', 'sale', 'brand', 'discount', 'link']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id','image','deal', 'feature', 'discount']"""

class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images, Additional_Informations)
    list_display = ('product_name', 'price', 'category', 'section')
    list_editable = ('category', 'section')

admin.site.register(Slider)
admin.site.register(Banner)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(Customer)