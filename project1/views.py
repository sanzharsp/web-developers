
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
import os.path
from django.db import transaction
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.base import reverse
from .forms import LoginView_Form_view,RegistrForm,CommentForm,Change_PasswordForm,New_Password,OrderForm,email
from .models import (Cart, Comment, Customer, Product, Category, subcategories,New_Recomedation,REKLAMA,CartProduct,NEWS_MODEL)
from django.urls import reverse_lazy
from django.views.generic import  View, ListView
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from .cartmixin import CartMixin
from .utils import recalc_cart,Randomaizer,ajax_utils_loaded
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from .utils import create_comments_tree,get_children,create_comments_tree_no_itereible,token_generator,token_generator_2,token_generator_password
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
import pytz
from .templatetags.comments_tree import comments_filter,comments_filter_children
import datetime




today = datetime.datetime.now()
Astana=today.astimezone(pytz.timezone('Asia/Almaty'))
DATA_TIME_FORMAT="%Y-%m-%d %H:%M:%S"

#для корзины
def cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            customer = Customer.objects.create(
                user=request.user
            )
        cart = Cart.objects.filter(owner=customer, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
    else:
        cart = Cart.objects.filter(for_anonymous_user=True).first()
        if not cart:
            cart = Cart.objects.create(for_anonymous_user=True)
    return cart


#для 
def none(request):
    cart=0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        cart = Cart.objects.filter(owner=customer, in_order=True).all()

    return cart

def discount(request):
    #логика скидок
    product_id_get=Product.objects.values('id')
    for i in range(0,product_id_get.count()):
        integers=product_id_get[i]['id']
        discount_view=Product.objects.get(id=integers)
        str_Astana_time=Astana.strftime(DATA_TIME_FORMAT)
        str_Data_0=discount_view.birth_date.strftime(DATA_TIME_FORMAT)
        str_Data=discount_view.discount_end_date.strftime(DATA_TIME_FORMAT)   
        New_products=datetime.datetime.strptime(str_Astana_time,DATA_TIME_FORMAT)-datetime.datetime.strptime(str_Data_0,DATA_TIME_FORMAT)>=datetime.timedelta(days=3,seconds=0,microseconds=0,milliseconds=0,minutes=0,hours=0,weeks=0)
        if (New_products):
            discount_view.new=False
            discount_view.save()

        if (datetime.datetime.strptime(str_Astana_time,DATA_TIME_FORMAT) >= datetime.datetime.strptime(str_Data,DATA_TIME_FORMAT) and discount_view.discount!=0 ):
            discount_view.price=discount_view.old_discount
            discount_view.discount=0
            discount_view.save()
#проверка почты
def verificate_email(request):
    # если ползеватель автаризован
    customer_verificate=None
    if request.user.is_authenticated:
        try:
            customer = User.objects.get(username=request.user)
            customer_verificate=Customer.objects.get(user=customer.id)
        except:
            customer_verificate=None
    return customer_verificate




#Авторизация 
class Users(CartMixin,LoginView):
    form_class = LoginView_Form_view
    template_name='login-register01.html'
    def get_context_data(self,*,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        return dict(list(context.items()))
    def get_success_url(self):
        return reverse_lazy('index')


# Выйти
class logout(LogoutView):
    next_page=reverse_lazy('index')


#Регистрация 
class Register(CartMixin, View):

    def get(self, request):
        form = RegistrForm(request.POST or None)
        categories=Category.objects.all()
        context = {
            'form': form,
            'cart': self.cart,
            'categories':categories
        }
        return render(request, 'login-register.html', context)

    def post(self, request):
        form = RegistrForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            password_for_email=form.cleaned_data['password']
            uidb64=urlsafe_base64_encode(force_bytes(new_user.pk))
            domain=get_current_site(request).domain
            link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(new_user)})
            activate_url='http://'+domain+link
            htmly= get_template('Email/email.html')
            d = { 'activate_url': activate_url,'user':new_user.username,'first_name':new_user.first_name,'last_name':new_user.last_name,'password':password_for_email}
            subject, from_email, to = 'Потверждение электронной почты','click@noreply.com', new_user.email
            text_content = 'None'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'cart': self.cart,
            'categories':categories
        }
        return render(request, 'login-register.html', context)    


#Верификация
class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
            users=Customer.objects.get(user_id=user)
            users.is_verificate=True
            users.save()
            if not token_generator.check_token(user,token):
                return redirect('/')

            if user.is_active:
                return redirect('/')
            user.is_active=True
            user.save()
            messages.success(request,'Ваш аккаунт активирован')
            return redirect('/')

        except Exception as excepts:
            print(excepts)
        return redirect('login')

#Повторная верификация 
class Verificaation_email_pavtor(View):
    
    def get(self, request):
        if request.user.is_authenticated:

            customer = User.objects.get(username=request.user)
            
            uidb64=urlsafe_base64_encode(force_bytes(customer.pk))
            domain=get_current_site(request).domain
            link=reverse('activatetwo',kwargs={'uidb64':uidb64,'token':token_generator_2.make_token(customer)})
            activate_url='http://'+domain+link
            htmly= get_template('Email/email.html')
            d = { 'activate_url': activate_url,'user':customer.username,'first_name':customer.first_name,'last_name':customer.last_name,'password':'Password already hashed'}
            subject, from_email, to = 'Потверждение электронной почты','click@noreply.com', customer.email
            text_content = 'None'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
        return HttpResponseRedirect('/')




#New password
class Change_Password(View):
    def get(self, request):
        form = Change_PasswordForm(request.POST or None)

        context = {
            'form': form,
   
        }
        return render(request, 'Change_Password.html', context)

        
    def post(self,request):
        
        form = Change_PasswordForm(request.POST or None)
        
        if form.is_valid():
            get_user = User.objects.get(username = request.POST['username'])
            get_email=request.POST['email']
            uidb64=urlsafe_base64_encode(force_bytes(get_user.pk))
            domain=get_current_site(request).domain
            linket=reverse('set_passwords',kwargs={'uidb64':uidb64,'token':token_generator_password.make_token(get_user)})
            activate_url='http://'+domain+linket

            htmly= get_template('Email/change_pochta.html')
            
            if get_user.email == get_email:
                d = { 'activate_url': activate_url,'first_name':get_user.first_name,'last_name':get_user.first_name}
                subject, from_email, to = 'Сброс пароля','click@noreply.com', get_user.email
                text_content = 'None'
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)

            messages.success(request, 'Вам отправлена на электронную почту ссылка на сброс пароля')
        context={
            'form': form,
        }
        return render(request, 'Change_Password.html', context)


class Set_Passwords(View):
    def get(self, request, *args, **kwargs):
        form = New_Password(request.POST or None)

        context = {
            'form': form,
   
        }
        return render(request, 'Change_Password_Set.html', context)

    def post(self,request,uidb64,token):
        id=force_str(urlsafe_base64_decode(uidb64))
        user_named=User.objects.get(pk=id)
        form = New_Password(request.POST or None)
        users=Customer.objects.get(user_id=user_named)
        
        if form.is_valid():
            
            user = User.objects.get(username = user_named)
            user.set_password(request.POST['password'])
            user.save()
            users.is_verificate=True
            users.save()
            messages.success(request, 'Ваш пароль был изменен, вы можете перейти в главную страницу')
        context = {
            'form': form,
   
        }
        return render(request, 'Change_Password_Set.html', context)


# Добавление в карзину
class ProductDetailView(CartMixin,View):
   
    def get(self, request,pk, *args, **kwargs):
        discount(request)
        products = Product.objects.all()    
        
        comments_counta=Comment.objects.all()[0:7]
  
        comments_count=Product.objects.get(id=pk).comments.all().count()
      
        result=create_comments_tree(comments_counta,pk)
     
      
        comment_form=CommentForm(request.POST or None)

        context = {
            
                'products': products,
                'pk':pk,
                'comments':result,
                'comment_form':comment_form,
                'comments_count':comments_count,
                'customer_verificate':verificate_email(request)
               
                }
        return render(request,'product-details-sticky-right.html', context)
    
    
    def post(self,request,pk):

        comment_form=CommentForm(request.POST)
        texts=request.POST.get('text')
        print(texts)
        print(comment_form)
        print(comment_form.is_valid())
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.user=request.user
            new_comment.text=comment_form.cleaned_data['text']
            new_comment.content_type=ContentType.objects.get(model='product')
            new_comment.object_id=pk
            new_comment.parent=None
            new_comment.timestamp=Astana.strftime(DATA_TIME_FORMAT)
            new_comment.is_child=False
            new_comment.save()
            print(new_comment)
            data={'new_parent_comment':comments_filter(create_comments_tree_no_itereible(new_comment,pk))}
            return JsonResponse(data,safe=False)
        
        return HttpResponseRedirect('/Product/{}/product_detail#1'.format(pk))
   
    def ajax_downolad_comment(self, request,pk):
        count = request.GET.get('val_count_com')
        count_ = request.GET.get('val_count_com_')
    

        data={'result':comments_filter(create_comments_tree(Comment.objects.all()[int(count_):int(count)],pk))}
        return JsonResponse(data,safe=False)
        

#при нажатий на категорию
class Product_categoty_all(CartMixin,View):
    def get(self, request,pk):
        discount(request)
        products = Product.objects.all()
        catigories=Category.objects.get(id=pk)
        catigories_all=Category.objects.all()
        context={'products':products,'catigories':catigories,'cart':cart(request),'catigories_all':catigories_all,'customer_verificate':verificate_email(request)}
        return render(request,'catigories.html', context)



def base_view(request,pk):
    comments=Product.objects.get(id=pk).comments.all()
    
    result=create_comments_tree(comments,pk)
    
    comment_form=CommentForm(request.POST or None)
    return render(request,'product-details-sticky-right.html',{'comments':result,'comment_form':comment_form})
 


def create_child_comment(request,pk):
    user_name=request.POST.get('user')
    current_id=request.POST.get('id')
    text=request.POST.get('text')
    user=User.objects.get(username=user_name)
    content_type=ContentType.objects.get(model='product')
    parent=Comment.objects.get(id=int(current_id))
    is_child=False if not parent else True
    Comment.objects.create(
        user=user,text=text,content_type=content_type,object_id=pk,
        parent=parent,is_child=is_child
    )
    comments_=Product.objects.get(id=pk).comments.all()[:1]
    resulys=comments_filter_children(get_children(comments_,pk))
    data={'current_id':current_id,'result':resulys}
    return JsonResponse(safe=False,data=data)

    
# система лайков продукта
class AddLike(View):
    def post(self,request,*args,**kwargs):
        posts=request.POST.get('post_id')
        post=Product.objects.get(pk=posts)
        is_like=False
        for like in post.likes.all():
            if like==request.user:
                is_like=True
                break  
        if not is_like:
            post.likes.add(request.user)
            post.value='Like'   
        if is_like:
            post.likes.remove(request.user)
            post.value='Unlike'
          
        post.save()
        
        data={  
                'is_like':is_like,
                'post_like':post.likes.all().count(),
        }
        return JsonResponse(data,safe=False)




#главный класс для корзины
class CartView(CartMixin, View):
    def get(self, request):
        discount(request)
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
            'customer_verificate':verificate_email(request)
        }
        return render(request, 'cart.html', context)



#Добавление товара в корзину
class AddToCartView(CartMixin, View):

    def get(self, request,*args,**kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.success(request, "Товар успешно добавлен")
        return HttpResponseRedirect('/cart/')


#Удаление товара 
class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.success(request, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')


#Удалить из корзины главной страницы
class DeleteFromIndex(CartMixin, View):
   
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
   
        return HttpResponseRedirect('/')


#Изменение количество товаров
class ChangeQTYView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty=1
        try:
            qty = int(request.POST.get('qty'))
        except:
            pass       
        if product.count_product >=qty:
            cart_product.qty = qty

            cart_product.save()
            recalc_cart(self.cart)
            data={'success':"Кол-во {} успешно изменено на {}".format(product.title,qty),'product':product.price,"final_price":self.cart.final_price}
            return JsonResponse(data,safe=False)
        else:
            data={'errors':"Продукта {} не хватает".format(product.title),}
            return JsonResponse(data,safe=False)


class Index(DetailView,CartMixin, View):
    #Главная страница
    def index(self, request, *args, **kwargs):

 

        #логика скидок
        discount(request)

        
        categories = Category.objects.all()
        products,best_stale,top_order=0,0,0
        recomndation_0,recomndation_1,recomndation_2,recomndation_0_subcotegeries,recomndation_1_subcotegeries,recomndation_2_subcotegeries=0,0,0,0,0,0
        try:
            products,best_stale,top_order = Product.objects.all()[:75],Product.objects.order_by('-orders')[:75],Product.objects.order_by('-likes')[:75]
        except:
            pass
        advertising=REKLAMA.objects.all()[:5]

        subcatigories=subcategories.objects.all()[:75]
        title=New_Recomedation.objects.all()[:7]
        
        index_random=Randomaizer().randoms(subcategories)
        try:
            recomndation_0=Product.objects.filter(subcategor=subcategories.objects.get(pk=index_random[0]))[:12]
            recomndation_1=Product.objects.filter(subcategor=subcategories.objects.get(pk=index_random[1]))[:12]
            recomndation_2=Product.objects.filter(subcategor=subcategories.objects.get(pk=index_random[2]))[:12]
            recomndation_0_subcotegeries=subcategories.objects.get(pk=index_random[0])
            recomndation_1_subcotegeries=subcategories.objects.get(pk=index_random[1])
            recomndation_2_subcotegeries=subcategories.objects.get(pk=index_random[2])
        except:
            pass
        

        context = {
               
                'cart':cart(request),
                'categories': categories,
                'products': products,
                'best_stale':best_stale,
                'top_order':top_order,
                'subcatigories':subcatigories,
                'title':title,
                'recomndation_0':recomndation_0,   
                'recomndation_1':recomndation_1,
                'recomndation_2':recomndation_2,
                'recomndation_0_subcotegeries':recomndation_0_subcotegeries,'recomndation_1_subcotegeries':recomndation_1_subcotegeries,'recomndation_2_subcotegeries':recomndation_2_subcotegeries,
                'customer_verificate':verificate_email(request),
                'advertising':advertising,
               
             
                }
        return render(request, 'index.html', context) 
        # except BaseException:
        #     return render(request, '404.html')

    def about(self,request):
        return render(request,'about.html' )

    def errors_404(self,request):
        return render(request,'404.html' )


    


    def shop(self,request,*args,**kwargs):
   
  
        
      
        products = Product.objects.all()[0:4]
    
           
        context={'cart':cart(request),'products':products,'customer_verificate':verificate_email(request),}
      
        return render(request,'shop.html',context)


    def ajax_shop(self,request):
        count = request.GET.get('val')
        count_ = request.GET.get('val_')
        data={'result':ajax_utils_loaded(request,Product.objects.all()[int(count_):int(count)])}
        return JsonResponse(data,safe=False)



    def shop_sidebar(self,request):
        return render(request,'shop-sidebar.html')

    def product_details_sticky_right(self,request):
        products = Product.objects.all()
        context={
            'products': products
        }
        return render(request,'product-details-sticky-right.html',context)
 
    def wishlist(self,request):
        return render(request,'wishlist.html')



    def team(self,request):
        return render(request,'team.html')


    def index_2(self,request):
        title=New_Recomedation.objects.all()
        discount(request)
        context={
                'title':title,
                'cart':cart(request),
            }
        return render(request,'index-2.html',context)

# block and contact
    def contact(self,request):
        return render(request,'contact.html' )

    def blog(self,request):
        return render(request,'blog.html' )

    def portfolio_gutter_box_3(self,request):
        return render(request,'portfolio-gutter-box-3.html' )

    def portfolio_gutter_full_wide_4(self,request):
        return render(request,'portfolio-gutter-full-wide-4.html' )
        
    def portfolio_card_box_3(self,request):
        return render(request,'portfolio-card-box-3.html' )

    def portfolio_masonry_3(self,request):
        return render(request,'portfolio-masonry-3.html' )

    def portfolio_gutter_masonry_fullwide_4(self,request):
        return render(request,'portfolio-gutter-masonry-fullwide-4.html' )

    def portfolio_gutter_box_3_carousel(self,request):
        return render(request,'portfolio-gutter-box-3-carousel.html' )

    def portfolio_justified_box_3(self,request):
        return render(request,'portfolio-justified-box-3.html' )

    def single_portfolio_gallery(self,request):
        return render(request,'single-portfolio-gallery.html' )
        
    def blog_2_col_rightsidebar(self,request):
        return render(request,'blog-2-col-rightsidebar.html' )
        
    def  blog_details_left_sidebar(self,request):
        return render(request,'blog-details-left-sidebar.html' )

    def blog_details(self,request):
        return render(request,'blog-details.html')

    def single_portfolio(self,request):
        return render(request,'single-portfolio.html')

#Поиск в сайте 

class SearchResultsView(View):
    def get(self,request,*args,**kwargs):
        query = self.request.GET.get('val')
        object_list__iexact = Product.objects.filter(
            Q(title__contains=query)
        )
        mas=[]
        for qery in object_list__iexact:
            mas.append(qery.title)
    
        data={'mas':mas}
    
        return JsonResponse(data,safe=False)

    def get_mod(self,request,*args,**kwargs):
        query = request.GET.get('quryset')
        object_list__iexact = Product.objects.filter(
            Q(title__contains=query)
        )
    
        return render(request,'extends.html',{'object_list':object_list__iexact})


class Filters(ListView):
    model=Product
    template_name='filter.html'

    def get(self,request,*args,**kwargs):
        name = self.kwargs.get('name')
        data = Product.objects.filter(category=name)
        filter_get_method=self.request.GET.get('qty')
        filter_get_method_2=self.request.GET.get('qty2')
        object_list = Product.objects.filter(price__range=(int(filter_get_method),int(filter_get_method_2)),category=name)
        context={'name':name,'data':data,'object_list':object_list}
        return render(request,'filter.html',context)

    

class Product_View (DetailView,CartMixin,View):
    def gets(self, request,*args,**kwargs):
        post_id = request.POST.get('post_id')      
        products=Product.objects.get(post_id)  
        discount(request)
        context = {
                'products_view': products,
                }
        return JsonResponse(context,safe=False)
  
#Orders
class MakeOrderView(CartMixin, View):
    
    def get(self, request,*args,**kwargs):
        discount(request)
        form = OrderForm(request.POST or None)
        customer = User.objects.get(username=request.user)
        customer_phone=Customer.objects.get(user=customer.id)  
        context = {
            'cart':cart(request),
            'form': form,
            'customer':customer,
            'phone':customer_phone.phone,
            'address':customer_phone.address,
        }
        return render(request,'checkout.html',context)


    @transaction.atomic
    def post(self, request,*args,**kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if customer.is_verificate == False:
            messages.error(request, 'Пожалуйста потвердите свою электронную почту')
            return HttpResponseRedirect('/make-order')
            
         

        if form.is_valid():
            
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            self.cart.save()
            new_order.save()
            customer.orders.add(new_order)
            new_order_cart=Cart.objects.filter(id=int(self.cart.id),in_order=True).first()
            for i in new_order_cart.products.all():
                if int(i.product.count_product)>=int(i.qty):
                    i.product.count_product=int(i.product.count_product)-int(i.qty)
                    i.product.orders=+1
                    i.product.save()
                else:
                    messages.error(request, 'Ммм все же товара не хватает')
                    return HttpResponseRedirect('/make-order')
            htmly= get_template('Email/orders.html')
            text_content = 'None'
           
           
             
            
            
            
            subject, from_email, to = 'Заказ','click@noreply.com',User.objects.get(username=request.user).email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            for i in new_order.cart.products.all():
                path=os.path.abspath(__file__).replace('project1\\views.py','media\\')+str(i.product.image)
                with open(path, mode='rb') as f:
                    image = MIMEImage(f.read())
                    msg.attach(image)
                   
            d={'customer':new_order.customer,'my_oreder':new_order.cart.products.all(),} 
            html_content = htmly.render(d)     
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
            messages.success(request, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/make-order')
        return HttpResponseRedirect('/make-order')

# Мои заказы
class MY_ORDERS(View):
    def get(self,request,*args,**kwargs):
        context={'my_oreder':none(request),'cart':cart(request),}
        return render(request,'my_orders.html',context)
     


#Эмайл рассылка 
class News_view(View):
    def post(self,request,*args,**kwargs):
        form=email(request.POST)
       
        if form.is_valid():
            NEWS_MODEL.objects.create(
                email=form.cleaned_data['email'],
                
            )
        
        data={'bool':form.is_valid()}
        return HttpResponseRedirect('index')