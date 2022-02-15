from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.db import models
import pytz
import random

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
            'timestamp':comment.timestamp.astimezone(pytz.timezone('Asia/Almaty')).strftime('%Y-%m-%d | %H:%M'),
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
            'timestamp':comment.timestamp.astimezone(pytz.timezone('Asia/Almaty')).strftime('%Y-%m-%d | %H:%M'),
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
        for i in range(1,s+1):
            result=random.randint(1,s)
            if result not in ran:
                ran.append(result)
        if len(ran)<s:
            for i in range(1,s*s):
                result=random.randint(1,s)
                if result not in ran:
                    ran.append(result)
        if len(ran)>s:
            d=s-len(ran)
            for end in range(1,d+1):
                result=random.randint(1,s)
                if result not in ran:
                    ran.append(result)
        return ran
        
        
