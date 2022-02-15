
# Подключаем компонент для работы с формой
from .models import Comment,Order,Category,subcategories,Product
from django import forms
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()

# класс для авторизаций

class LoginView_Form_view(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя','class':'text-field__input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Пароль",'class':'text-field__input','id':"password-input-login",'name':"password"}))
    

class Change_PasswordForm(forms.Form):    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя','class':'text-field__input'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email(почта)",'class':'text-field__input'}))
    class Meta:
        model = User
        fields = ('username','email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = 'Введите ваш существующи логин'
  
        self.fields['email'].help_text = 'Введите email(почта) каторую вы зарегестрировали'
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if not User.objects.filter(username=username).first():
            
            raise forms.ValidationError(
                
                f'Имя {username} нет в системе'
                
            )
        return username
    def clean_email(self):
        email = self.cleaned_data['email']

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Данный почтовый адрес  незарегистрирован в системе'
            )
        return email
  

class New_Password(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Пароль",'class':'text-field__input','id':"password-input-login",'name':"password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Подвердите пароль",'class':'text-field__input','id':"password-input-login-confirm",'name':"password"}))
    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].help_text = 'Введите новый пароль'
  
        self.fields['confirm_password'].help_text = 'Потвердите пароль'

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if len(password)<8:
            raise forms.ValidationError(f'Пароль должен содержать не менее 8 символов')
        if password != confirm_password :
            raise forms.ValidationError(f'Пароли не совпадают')
        return self.cleaned_data

# Создаём класс формы
class RegistrForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Придумайте имя пользователя','class':'text-field__input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Подвердите пароль",'class':'text-field__input','id':"password-input-login-confirm",'onChange':'checkPasswordMatch()','name':"password"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Введите пароль",'class':'text-field__input','id':"password-input-login",'name':"password"}))
    phone = forms.CharField(widget=forms.TextInput( attrs={'placeholder':"+7(---)-- -- --",'class':'text-field__input'}))
    address = forms.CharField(widget=forms.TextInput( attrs={'placeholder':"Введите ваш адресс",'class':'text-field__input'}))
    first_name=forms.CharField(widget=forms.TextInput( attrs={'placeholder':"Имя",'class':'text-field__input'}))
    last_name=forms.CharField(widget=forms.TextInput( attrs={'placeholder':"Фамилия",'class':'text-field__input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email(почта)",'class':'text-field__input'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин'
        self.fields['username'].help_text = 'Придумайте логин но он должен быть не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['address'].label = 'Адрес'
        self.fields['email'].help_text = 'Например admin@gmail.com'
        self.fields['email'].label = 'Электронная почта'


    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['su', 'org']:
            raise forms.ValidationError(
                
                f'Регистрация для домена {domain} невозможна'
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Данный почтовый адрес уже зарегистрирован в системе'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        
        if User.objects.filter(username=username).exists():
            
            raise forms.ValidationError(
                
                f'Имя {username} занято'
                
            )
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if len(password)<8:
            raise forms.ValidationError(f'Пароль должен содержать не менее 8 символов')
        if password != confirm_password :
            raise forms.ValidationError(f'Пароли не совпадают')
        return self.cleaned_data
    


    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']
        

class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')


        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model=Comment
        fields=['text']

class OrderForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )



#######################################################################################

# ###################        # ########### #          # # # #                # # # #
# ###################        # ########### #          # #  # #              # #  # #
# #                          # #         # #          # #   # #            # #   # #
# #                          # #         # #          # #    # #         # #     # #  
# #                          # #         # #          # #     # #       # #      # #
# #                          # ########### #          # #      # #    # #        # #
# #                          # ########### #          # #       # # # #          # #
# #                          # ## #                   # #         # #            # #
# #                          # # # #                  # #                        # #
# #                          # #  # #                 # #                        # #
# #################          # #   # #                # #                        # #
###################          # #    # #               # #                        # #

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


    category = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategor =forms.ModelChoiceField(queryset=subcategories.objects.all())
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название категория','class':'text-field__input'}))
    image=forms.ImageField()
    images_2=forms.ImageField(required=False)
    images_3=forms.ImageField(required=False)
    description=RichTextField()
    price=forms.DecimalField()
    count_product=forms.DecimalField()
    history_price=forms.DecimalField()
    discount=forms.DecimalField(initial=0)
    discount_end_date=forms.DateTimeField(initial='04.02.2022')
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


class ProductFormCRMset(forms.ModelForm):


    category = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategor =forms.ModelChoiceField(queryset=subcategories.objects.all())
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название категория','class':'text-field__input'}))
    image=forms.ImageField()
    images_2=forms.ImageField(required=False)
    images_3=forms.ImageField(required=False)
    description=RichTextField()
    price=forms.DecimalField()
    count_product=forms.DecimalField()
    history_price=forms.DecimalField()
    discount=forms.DecimalField(initial=0)
    discount_end_date=forms.DateTimeField(initial='04.02.2022')
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