
from project1.models import ( Product, Category, subcategories)
from .crm_forms import(CategoryCRM_Form,CategoryCRM_SET_Form,ProductFormCRM,ProductCRM_SET_FORM,subcatigoriesFORMCRM)
from project1.views import cart
from django.views.generic import  View
from django.shortcuts import  render
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
import uuid


#######################################################################################

# ###################        # ########### #          # # # #                # # # #
# ###################        # ########### #          # #  # #              # #  # #
# #                          # #         # #          # #   # #            # #   # #
# #                          # #         # #          # #    # #         # #     # #  
# #                          # #         # #          # #     # #       # #      # #
# #                          # ########### #          # #      # #    # #        # #
# #                          # ########### #          # #       # # # #          # #
# #                          # ## #                   # #         # #            # #
# #                          # #   # #                # #                        # #
# #                          # #     # #              # #                        # #
# #################          # #      # #             # #                        # #
###################          # #        # #           # #                        # #

#########################################################################################
# скидка
def data_product_settings(update):
    update.old_discount=update.price
    if int(update.discount) != 0:
        update.price = update.price - update.price*(update.discount/100)
        update.history_price=update.old_discount
    
    update.save()
    
# начальная страница
class Iindex_CRM(View):
    
    def get(self,request):
        if request.user.is_superuser:
            return render(request,'CRM/index/CRM_INDEX.html')
        else:
            return HttpResponseRedirect('login-register')

# Добавление котегорию

class CategoryCRM(View):
    
    def get(self,request):
        if request.user.is_superuser :
            categories_view=Category.objects.all()
            form = CategoryCRM_Form(request.POST or None)
            context={
            'form':form,
            'category':categories_view,
            'cart':cart(request)
            }
            return render(request,'CRM/Category.html',context)
        else:
            return HttpResponseRedirect('login-register')

    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form = CategoryCRM_Form(request.POST,request.FILES)
            if form.is_valid():
                Category.objects.create (
                name=form.cleaned_data['name'],
                slug=str(uuid.uuid4())+str(int(Category.objects.all().count())+1),
                image=form.cleaned_data['image'],
            )
                messages.success(request, 'Категория успешно создана')
                return HttpResponseRedirect('/category_add')
        else:
            return HttpResponseRedirect('login-register')
        
        return HttpResponseRedirect('/category_add')

# Редактирование категорий

class CategorySetCRM(View):
    def get(self, request,slug, *args, **kwargs):
        if request.user.is_superuser:
            form=CategoryCRM_SET_Form(request.POST or None)
            category__val=Category.objects.get(slug=slug)
            context={
                'category':category__val,
                'form':form,
                'cart':cart(request)
            }
            return render(request,'CRM/SET/category_set__CRM.html',context)
        else:
            return HttpResponseRedirect('login-register')
    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form=CategoryCRM_SET_Form(request.POST,request.FILES)
            category__val=Category.objects.filter(slug=kwargs.get('slug'))
            if form.is_valid():
                
                category__val.update(
                name=form.cleaned_data['name'],
                image=form.cleaned_data['image']
                )
                
                messages.success(request, 'Категория успешно изменено')
                return HttpResponseRedirect('/category_set/{}'.format(kwargs.get('slug')))
            
        else:
            return HttpResponseRedirect('login-register')
        return HttpResponseRedirect('/category_set/{}'.format(kwargs.get('slug')))
#Удаление категорий

class Delete_CategoryCRM(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser :
            category__val=Category.objects.get(slug=kwargs.get('slug'))
            category__val.delete()
            return HttpResponseRedirect('/category_add')
        else:
            return HttpResponseRedirect('login-register')




# Добавление продуктов

class ProductViewCRM(View):
    
    def get(self,request):
        if request.user.is_superuser :
            product_view=Product.objects.all()
            category=Category.objects.all()
            context={
            'product_view':product_view,
            'category_view':category,
            'cart':cart(request)
            }
            return render(request,'CRM/Product_create.html',context)
        else:
            return HttpResponseRedirect('login-register')

    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form = ProductFormCRM(request.POST,request.FILES)
            if form.is_valid():

                settings_product=Product.objects.create (
                slug=str(uuid.uuid4())+str(int(Product.objects.all().count())+1),
                category=form.cleaned_data['category'],
                subcategor=form.cleaned_data['subcategor'],
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'],
                images_2=form.cleaned_data['images_2'],
                images_3=form.cleaned_data['images_3'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                count_product=form.cleaned_data['count_product'],
                history_price=form.cleaned_data['history_price'],
                discount=form.cleaned_data['discount'],
                discount_end_date=form.cleaned_data['discount_end_date'],
                new=form.cleaned_data['new'],
                

                )
                data_product_settings(settings_product)
                messages.success(request, 'Продукт успешно создан')
                return HttpResponseRedirect('/products_add')
        else:
            return HttpResponseRedirect('login-register')
        
        return HttpResponseRedirect('/products_add')

# Редактирование продукта

class ProductViewCRMset(View):
    def get(self, request,slug, *args, **kwargs):

        if request.user.is_superuser:
            category=Category.objects.all()
            subcotigory=subcategories.objects.all()
            product__val=Product.objects.get(slug=slug)
            context={
                'cart':cart(request),
                'product':product__val,
                'category_view':category,
                'subcotigories':subcotigory,
                
            }
            return render(request,'CRM/SET/product_set__CRM.html',context)
        else:
            return HttpResponseRedirect('login-register')
    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form=ProductCRM_SET_FORM(request.POST,request.FILES)
            

            if form.is_valid():
                product__val=Product.objects.filter(slug=kwargs.get('slug'))
                product__val.update(
                category=form.cleaned_data['category'].id,
                subcategor=form.cleaned_data['subcategor'].id,
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'],
                images_2=form.cleaned_data['images_2'],
               images_3=form.cleaned_data['images_3'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                count_product=form.cleaned_data['count_product'],
                history_price=form.cleaned_data['history_price'],
                discount=form.cleaned_data['discount'],
                discount_end_date=form.cleaned_data['discount_end_date'],
                new=form.cleaned_data['new'])
                for i in product__val:
                    data_product_settings(i)
                
                
        

                messages.success(request, 'Продукт успешно изменен')
                return HttpResponseRedirect('/product_set/{}'.format(kwargs.get('slug')))
        else:
            return HttpResponseRedirect('login-register')
        return HttpResponseRedirect('/product_set/{}'.format(kwargs.get('slug')))


#Удаление продукта 
class Delete_ProductCRM(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser                                                                                                                            :
            product__val=Product.objects.get(slug=kwargs.get('slug'))
            product__val.delete()
            return HttpResponseRedirect('/products_add')
        else:
            return HttpResponseRedirect('login-register')



# Дабовление Подкатегорий

class SubcatigoriesCRM(View):
    def get(self,request):
        if request.user.is_superuser :
            form = subcatigoriesFORMCRM(request.POST,request.FILES)
            subcategories_val=subcategories.objects.all()
            context={
            'form':form,
            'subcatigory':subcategories_val,
            'cart':cart(request)
            }
            return render(request,'CRM/subcatigory.html',context)
        else:
            return HttpResponseRedirect('login-register')

    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form = subcatigoriesFORMCRM(request.POST,request.FILES)
            if form.is_valid():
                subcategories.objects.create (
                category_product=form.cleaned_data['category_product'],
                subcategories_slug=str(uuid.uuid4())+str(int(subcategories.objects.all().count())+1),
                subcategory=form.cleaned_data['subcategory'],
            )
                messages.success(request, 'Подкатигория успешно создана')
                return HttpResponseRedirect('/subcatigory_add')
        else:
            return HttpResponseRedirect('login-register')
        
        return HttpResponseRedirect('/subcatigory_add')



#Редактирование Подкатегорий

class SubcatigoriesSetCRM(View):
    def get(self, request,slug, *args, **kwargs):
        if request.user.is_superuser:
            category=Category.objects.all()
            subcatigory__val=subcategories.objects.get(subcategories_slug=slug)
            context={
                'subcatigory':subcatigory__val,
                'cart':cart(request),
                'category':category
            }
            return render(request,'CRM/SET/subcatogory_set__CRM.html',context)
        else:
            return HttpResponseRedirect('login-register')
    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form=subcatigoriesFORMCRM(request.POST,request.FILES)
            subcategories__val=subcategories.objects.filter(subcategories_slug=kwargs.get('slug'))
            if form.is_valid():
                
                subcategories__val.update(
                category_product=form.cleaned_data['category_product'],
                subcategory=form.cleaned_data['subcategory']
                )
                
                messages.success(request, 'Подкатигория успешно изменено')
                return HttpResponseRedirect('/subcatigory_set/{}'.format(kwargs.get('slug')))
            
        else:
            return HttpResponseRedirect('login-register')
        return HttpResponseRedirect('/subcatigory_set/{}'.format(kwargs.get('slug')))

# Удаление Подкатигория
class Delete_SubcatigoriesCRM(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser                                                                                                                            :
            subcategories_val=subcategories.objects.get(subcategories_slug=kwargs.get('slug'))
            subcategories_val.delete()
            return HttpResponseRedirect('/subcatigory_add')
        else:
            return HttpResponseRedirect('login-register')

#ajax продукта 
class AJAXCRMCategory(View):
    def get(self,request,*args, **kwargs):
        post_id = request.GET.get('val')
        mas=[]
        mas_name=[]
        value=subcategories.objects.filter(category_product=Category.objects.get(id=post_id))
        
        for i in value:
            mas.append(i.id)
            mas_name.append(i.subcategory)

        data={
            'mas':mas,
            'mas_name':mas_name
        }

        return JsonResponse(data,safe=False)