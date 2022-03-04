from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.db import models
from .models import Product
import pytz
from django.middleware.csrf import get_token
import random
import datetime
today = datetime.datetime.today()
Astana=today.astimezone(pytz.timezone('Asia/Almaty'))
DATA_TIME_FORMAT="%Y-%m-%d | %H:%M:%S"
str_Astana_time=Astana.strftime(DATA_TIME_FORMAT)

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

class AppTokenGenerator_2(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

class AppTokenGenerator_Passwords(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk)+text_type(timestamp))

token_generator=AppTokenGenerator()
token_generator_2=AppTokenGenerator_2()
token_generator_password=AppTokenGenerator_Passwords()


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()


def get_children(qs_child,pk):
    res=[]
    for comment in qs_child:
       
        c={
            'id':comment.id,
            'text':comment.text,
            'timestamp':comment.timestamp.astimezone(pytz.timezone('Asia/Almaty')).strptime(str_Astana_time,DATA_TIME_FORMAT),
            'author':comment.user,
            'object_id_models':comment.object_id,
            'is_child':comment.is_child,
            'parent_id':comment.parent,
            'content_type':comment.content_type,
            'pk':pk
            }
        if comment.comment_children.exists():
             c['children']=get_children(comment.comment_children.all(),pk)
        res.append(c)
    return res

    
def create_comments_tree(qs,pk):
    res=[]
    for comment in qs:
        c={
            'id':comment.id,
            'text':comment.text,
            'timestamp':comment.timestamp.astimezone(pytz.timezone('Asia/Almaty')).strptime(str_Astana_time,DATA_TIME_FORMAT),
            'author':comment.user,
            'object_id_models':comment.object_id,
            'is_child':comment.is_child,
            'parent_id':comment.parent,
            'content_type':comment.content_type,
            'pk':pk
            
        }

        if comment.comment_children:
            c['children']=get_children(comment.comment_children.all(),pk)
        if not comment.is_child:
            res.append(c)
    
   
    return res

#рандомизация главной страницы
class Randomaizer():
    def randoms(self,s):
        ran=[]
        for i in s.objects.all():
            ran.append(i.id)
        return random.sample(ran,len(ran))
        
#количество продуктов
def count_models_data():
    return Product.objects.all().count


#ajax подгрузка
def ajax_utils_loaded(request,products):
      
    
    result="""
    <div   class="product__list another-product-style">
    {}
    </div>
    """
    
    
    mas=''
    if_discount=''
    if_new=''
    user=''
    product_none=''
    forms_=''
    for i in products:
        if i.discount != 0:
            if_discount+='<div class="sale_discount">- {product_discount}% {date_discount}</div>'.format(product_discount=i.discount,date_discount=i.discount_end_date )
        if i.new:
            if_new="""<div class="sale_new">новинка</div>"""           
            
        if request.user.is_authenticated:
            user="""
                <li><a href="/Product/{id}/product_view" data-toggle="modal"  data-target="#productModal{id}" title="Quick View" class="quick-view modal-view detail-link" ><span class="ti-plus"></span></a></li>
                <li><a title="Add TO Cart" href="add-to-cart/{slug}/"><span class="ti-shopping-cart"></span></a></li>
                <li><a title="Wishlist" href="/wishlist/"><span class="ti-heart"></span></a></li>
                """.format(id=i.id,slug=i.slug)
            forms_="""
                                
                    <div id="id_str{id}" class="class_str{id}">
                    {value}
                       </div>
                        <form method="POST" class="like-form{id}" id='{id}'>
                        <input type="hidden" name="csrfmiddlewaretoken" value="{token_crsf}">
                                            <input type="hidden" name="next" value="{path}" >
                                            <button class="button" onclick="Like_dislike_ajax('{id}');return false;" type="submit" >
                                            <div class="hand">
                                            <div class="thumb"></div>
                                            </div>
                                            <span><div id="like{id}" class="likes{id}">{counts__S}</div></span>
                                           
                                        </button>
                                       
                                        </form>        
                    """.format(id=i.id,value=i.value,path=request.path,counts__S=i.likes.all().count(),token_crsf=get_token(request))
        if request.user.is_authenticated==False:
            user="""
                <li><a data-toggle="Вы не авторизованы" data-target="/login-register01/" title="Вы не авторизованы" class="quick-view modal-view detail-link" href="/login-register01/"><span class="ti-plus"></span></a></li>
                <li><a title="Вы не авторизованы" href="/login-register01/"><span class="ti-shopping-cart"></span></a></li>
                <li><a title="Вы не авторизованы" href="/login-register01/"><span class="ti-heart"></span></a></li>
                """
        if i.count_product == 0:
            product_none='<h2><a style="color:red;">нет в наличий</a></h2>'
        
                    
                                                            
                                    
        mas+="""
                          <div  class="col-md-3 single__pro col-lg-3 cat--1 col-sm-4 col-xs-12">          
                             <div class="product foo">
                                               
                      
                                                
                                                
                                                <div class="product__inner">
                                                    <div class="pro__thumb">
                                                        <a href="Product/{id}/product_detail">
                                                           
                                                           <div class="product_discount" >
                                                   {if_discount}
                                                   {if_new}
                                                   <img src="{image}"  alt="product images">
                                                    </div> 
                                               
                                                        </a>
                                                    </div>
                                                    <div class="product__hover__info">
                                                        <ul class="product__action">
                                                           {user_auth}
                                                           
                                                        </ul>
                                                    </div>
                                                </div>
                                               
                                                <div class="product__details">
                                                    <h2><a href="">{title}</a></h2>
                                                    <h2><a style="color:red;">{count_product} шт</a></h2>
                                                        {none_product}
                                                    <ul class="product__price">
                                                    <li class="old__price">{history_price} тенге</li>
                                                    <li class="new__price">{price} тенге</li>
                                                        
                                                        <br>
                                                       {forms}
                                            
                                                      
                                                    
                                                        
                                                    </ul>
                                                    
                                                </div>
                                           
                                              
                                            </div>
                                        </div>
                        """.format(id=i.id,if_discount=if_discount,image=i.image.url,user_auth=user,title=i.title,count_product=i.count_product,none_product=product_none,history_price=i.history_price,price=i.price,forms=forms_,if_new=if_new)

    result.format(mas)
    return result.format(mas)