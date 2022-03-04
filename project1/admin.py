from django.contrib import admin
from django.forms import ModelForm
from .models import *
from PIL import Image
from django import forms



#admin.site.register(object)
class ProductAdminForm(ModelForm):
   
   
    MIN_IMAGE=(250,250)
    MIN_VOLIUM=2097152


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['subcategor'].help_text='Категории у подкатегорий и продукта должны совподать'
        self.fields['image'].help_text='Минимальное разрешение изображения {}'.format(self.MIN_IMAGE)
     
       
    def clean_image(self):
        image=self.cleaned_data['image']
        image_=Image.open(image)
        min_width,min_height=self.MIN_IMAGE
        sizeimg=round(image.size/1024000,1)
        if image.size > self.MIN_VOLIUM:
            raise ValidationError('Загружаемое изображение({}мб) больше 2 мб'.format(sizeimg))
        if image_.width<min_width or image_.height<min_height:
            raise ValidationError('Загружаемое изображение меньше минимального \U0001F62A')
        
        return image


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug','birth_date')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'phone','address','birth_date')


class ProductChoiceField(forms.ModelChoiceField):
    pass


class ProductAdmin(admin.ModelAdmin): 
    form=ProductAdminForm
    list_display=('id','title','category','slug','price','birth_date')

# Исправить Админка 0
    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
       
        #if db_field.name == "subcategor":
            #kwargs["queryset"] =subcategories.objects.filter(id=1)
            
        #return super().formfield_for_foreignkey(db_field, request, **kwargs)


class subcategoriesAdmin(admin.ModelAdmin):
    list_display=('id','subcategory','birth_date')

    
class New_RecomedationAdmin(admin.ModelAdmin):
    list_display=('black_text','red_text','birth_date')


class New_Recomendations2Admin(admin.ModelAdmin):
    list_display=('black_text','red_text','birth_date')

admin.site.register(REKLAMA)

admin.site.register(New_Recomedation,New_RecomedationAdmin)

admin.site.register(CartProduct)

admin.site.register(Order)

admin.site.register(Cart)

admin.site.register(Customer,CustomerAdmin)

admin.site.register(Category,CategoryAdmin)

admin.site.register(subcategories,subcategoriesAdmin)

admin.site.register(Product,ProductAdmin)

admin.site.register(Comment)

admin.site.register(NEWS_MODEL)

admin.site.site_header="Админ панель для интерент магазина"

admin.site.site_title="Администрирование интернет магазина"

