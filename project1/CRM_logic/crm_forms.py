from project1.models import Category,subcategories,Product
from django import forms
from ckeditor.fields import RichTextField
from project1.views import today,Astana,DATA_TIME_FORMAT
import datetime
#######################################################################################

# ###################        # ########### #          # # # #                # # # #
# ###################        # ########### #          # #  # #              # #  # #
# #                          # #         # #          # #   # #            # #   # #
# #                          # #         # #          # #    # #         # #     # #  
# #                          # #         # #          # #     # #       # #      # #
# #                          # ########### #          # #      # #    # #        # #
# #                          # ########### #          # #       # # # #          # #
# #                          # ## #                   # #         # #            # #
# #                          # #  # #                  # #                        # #
# #                          # #    # #                 # #                        # #
# #################          # #      # #                # #                        # #
###################          # #        # #               # #                        # #

#########################################################################################



# models Category forms

class CategoryCRM_Form(forms.ModelForm):


    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название категория','class':'text-field__input'}))
    image = forms.ImageField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название категория'
        self.fields['image'].label = 'Изображение'

    class Meta:
        model = Category
        fields = (
            'name','image'
        )

# models Category Set forms

class CategoryCRM_SET_Form(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название категория'
        self.fields['image'].label = 'Изображение'

    class Meta:
        model = Category
        fields = (
            'name','image'
        )

# models Product forms

class ProductFormCRM(forms.ModelForm):
    SET=Category.objects.all()

    category = forms.ModelChoiceField(queryset=SET)
    subcategor =forms.ModelChoiceField(queryset=subcategories.objects.all())
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название продукта','class':'text-field__input'}))
    image=forms.ImageField()
    images_2=forms.ImageField(required=False)
    images_3=forms.ImageField(required=False)
    description=RichTextField()
    price=forms.DecimalField()
    count_product=forms.DecimalField()
    history_price=forms.DecimalField()
    discount=forms.DecimalField()
    discount_end_date=forms.DateTimeField(initial=Astana.strftime(DATA_TIME_FORMAT),widget=forms.DateTimeInput())
    new=forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].label = 'Категория'
        self.fields['subcategor'].label = 'Подкатегория'
        self.fields['title'].label = 'Название продукта'
        self.fields['image'].label = 'Главная изображение товара'
        self.fields['images_2'].label = 'Дочерние изображения'
        self.fields['images_3'].label = 'Дочерние изображения'
        self.fields['description'].label = 'Описание'
        self.fields['price'].label = 'Цена товара'
        self.fields['count_product'].label = 'Количество товара'
        self.fields['history_price'].label = 'Старая цена'
        self.fields['discount'].label = 'Скидка в процентах'
        self.fields['discount_end_date'].label = 'Дата окончания скидки'
        self.fields['new'].label = 'Новый продукт'
    class Meta:
        model = Product
        fields = (
            'category','subcategor','title','image','images_2','images_3','description','price','count_product','history_price','discount','discount_end_date','new'
        )

#Редактирование  продукта
class ProductCRM_SET_FORM(forms.ModelForm):
    SET=Category.objects.all()

    category = forms.ModelChoiceField(queryset=SET)
    subcategor =forms.ModelChoiceField(queryset=subcategories.objects.all())
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название продукта','class':'text-field__input'}))
    image=forms.ImageField()
    images_2=forms.ImageField(required=False)
    images_3=forms.ImageField(required=False)
    description=RichTextField()
    price=forms.DecimalField()
    count_product=forms.DecimalField()
    history_price=forms.DecimalField()
    discount=forms.DecimalField()
    discount_end_date=forms.DateTimeField()
    new=forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].label = 'Категория'
        self.fields['subcategor'].label = 'Подкатегория'
        self.fields['title'].label = 'Название продукта'
        self.fields['image'].label = 'Главная изображение товара'
        self.fields['images_2'].label = 'Дочерние изображения'
        self.fields['images_3'].label = 'Дочерние изображения'
        self.fields['description'].label = 'Описание'
        self.fields['price'].label = 'Цена товара'
        self.fields['count_product'].label = 'Количество товара'
        self.fields['history_price'].label = 'Старая цена'
        self.fields['discount'].label = 'Скидка в процентах'
        self.fields['discount_end_date'].label = 'Дата окончания скидки'
        self.fields['new'].label = 'Новый продукт'
    class Meta:
        model = Product
        fields = (
            'category','subcategor','title','image','images_2','images_3','description','price','count_product','history_price','discount','discount_end_date','new'
        )
