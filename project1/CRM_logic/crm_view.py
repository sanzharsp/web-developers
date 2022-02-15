
from project1.models import ( Product, Category, subcategories)
from .crm_forms import(CategoryCRM_Form,CategoryCRM_SET_Form,ProductFormCRM,ProductCRM_SET_FORM)
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
# #                          # #    # #               # #                        # #
# #################          # #     # #              # #                        # #
###################          # #      # #             # #                        # #

#########################################################################################

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
                slug=uuid.uuid4(),
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
            category__val=Category.objects.get(slug=kwargs.get('slug'))
            if form.is_valid():
                category__val.name=form.cleaned_data['name']
                category__val.image=form.cleaned_data['image']
                category__val.save()
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
            form = ProductFormCRM(request.POST or None)
            product_view=Product.objects.all()


  
            
            context={
            'form':form,
            'product_view':product_view,
            'cart':cart(request)
            }
            return render(request,'CRM/Product_create.html',context)
        else:
            return HttpResponseRedirect('login-register')

    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form = ProductFormCRM(request.POST,request.FILES)
            if form.is_valid():
                Product.objects.create (
                slug=uuid.uuid4(),
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
                messages.success(request, 'Продукт успешно создан')
                return HttpResponseRedirect('/products_add')
        else:
            return HttpResponseRedirect('login-register')
        
        return HttpResponseRedirect('/products_add')

# Редактирование продукта

class ProductViewCRMset(View):
    def get(self, request,slug, *args, **kwargs):

        if request.user.is_superuser:
            form=ProductCRM_SET_FORM(request.POST or None)
            category=Category.objects.all()
            subcotigory=subcategories.objects.all()
            
            product__val=Product.objects.get(slug=slug)
            filters=subcategories.objects.filter(category_product=Category.objects.get(id=product__val.category.id))
         
                 

            context={
                'cart':cart(request),
                'product':product__val,
                'form':form,
                'category_view':category,
                'filters':filters,
                'subcotigories':subcotigory,
                
            }
            return render(request,'CRM/SET/product_set__CRM.html',context)
        else:
            return HttpResponseRedirect('login-register')
    def post(self, request,*args, **kwargs):
        if request.user.is_superuser:
            form=ProductCRM_SET_FORM(request.POST,request.FILES)
            product__val=Product.objects.get(slug=kwargs.get('slug'))

            if form.is_valid():
                
                product__val.id=product__val.id
                product__val.category=Category.objects.get(id=request.POST['category']),
                product__val.subcategor=form.cleaned_data['subcategor'],
                product__val.title=form.cleaned_data['title'],
                product__val.image=form.cleaned_data['image'],
                product__val.images_2=form.cleaned_data['images_2'],
                product__val.images_3=form.cleaned_data['images_3'],
                product__val.description=form.cleaned_data['description'],
                product__val.price=form.cleaned_data['price'],
                product__val.count_product=form.cleaned_data['count_product'],
                product__val.history_price=form.cleaned_data['history_price'],
                product__val.discount=form.cleaned_data['discount'],
                product__val.discount_end_date=form.cleaned_data['discount_end_date'],
                product__val.new=form.cleaned_data['new'],
                product__val.save()
                messages.success(request, 'Продуст успешно изменен')
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

        print(value)
        data={
            'mas':mas,
            'mas_name':mas_name
        }

        return JsonResponse(data,safe=False)