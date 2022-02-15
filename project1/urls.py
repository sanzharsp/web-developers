from django.urls import path

from .import views

#base view
from .views import (
    base_view,
    create_child_comment,
    create_comment,
    MY_ORDERS,
    logout,
    Users,
    Register,
    ProductDetailView,
    AddLike,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    DeleteFromIndex,
    SearchResultsView,
    VerificationView,
    Verificaation_email_pavtor,
    Change_Password,
    Set_Passwords,
    MakeOrderView,
    Product_categoty_all,
    Filters,
)

#CRM
from .CRM_logic.crm_view import(
    Iindex_CRM,
    CategoryCRM,
    ProductViewCRM,
    CategorySetCRM,
    Delete_CategoryCRM,
    AJAXCRMCategory,
    ProductViewCRMset,
    
    Delete_ProductCRM,
)


urlpatterns = [
    path('',views.Index().index,name='index'),

    path('404_ERORRS',views.Index().errors_404,name='ERORRS_404'),

    path('about',views.Index().about,name='about'),

    path('shop',views.Index().shop,name='shop'),

    path('shop-sidebar',views.Index().shop_sidebar, name='shop-sidebar'),

    path('product-details-sticky-right',views.Index().product_details_sticky_right,name='product-details-sticky-right'),

    path('wishlist',views.Index().wishlist,name='wishlist'),

    path('team',views.Index().team,name='team'),

    path('Product/<int:pk>/product_detail',ProductDetailView.as_view(),name='product_detail'),

    path('index-2',views.Index().index_2,name='index_2'),
    
    path('Product/<int:pk>/like',AddLike.as_view(), name='like'),

    path('Product/<int:pk>/product_view',views.Product_View().gets, name='product_view'),

    path('contact',views.Index().contact,name='contact'),

    path('blog',views.Index().blog,name='blog'),

    path('cportfolio-gutter-box-3',views.Index().portfolio_gutter_box_3,name='portfolio-gutter-box-3'),

    path('portfolio-gutter-full-wide-4',views.Index().portfolio_gutter_full_wide_4,name='portfolio-gutter-full-wide-4'),
    
    path('portfolio-card-box-3',views.Index().portfolio_card_box_3,name='portfolio-card-box-3'),

    path('portfolio-masonry-3',views.Index().portfolio_masonry_3,name='portfolio-masonry-3'),

    path('portfolio-gutter-masonry-fullwide-4',views.Index().portfolio_gutter_masonry_fullwide_4,name='portfolio-gutter-masonry-fullwide-4'),

    path('portfolio-gutter-box-3-carousel',views.Index().portfolio_gutter_box_3_carousel,name='portfolio-gutter-box-3-carousel'),

    path('portfolio-justified-box-3',views.Index().portfolio_justified_box_3,name='portfolio-justified-box-3'),

    path('single-portfolio-gallery',views.Index().single_portfolio_gallery,name='single-portfolio-gallery'),

    path ('single-portfolio', views.Index().single_portfolio,name="single-portfolio"),

    path('blog-2-col-rightsidebar',views.Index().blog_2_col_rightsidebar,name='blog-2-col-rightsidebar'),

    path('blog-details-left-sidebar',views.Index().blog_details_left_sidebar,name='blog-details-left-sidebar'), 

    path('blog-details', views.Index().blog_details,name="blog-details"),

    #Детализация категорий

    path('catigories/<int:pk>', Product_categoty_all.as_view(),name="catigories"),

    #Ригистрация
    
    path('login-register01', Users.as_view() ,name='login-register01'),

    path('login-register', Register.as_view(),name='login-register'),

    path('login', Register.as_view(),name='login'),
    
    #Верификация

    path('activate/<uidb64>/<token>', VerificationView.as_view(),name='activate'),

    #Повторная верификация 

    path('activate_2', Verificaation_email_pavtor.as_view(),name='activate_2'),

    path('activatetwo/<uidb64>/<token>', VerificationView.as_view(),name='activatetwo'),
    
    #Сброс пароля

    path('set_passwords/<uidb64>/<token>', Set_Passwords.as_view(),name='set_passwords'),

    #Сброс пароля

    path('change_password', Change_Password.as_view(),name='change_password'),
    
    #Выход

    path('logout', logout.as_view(), name='logout_page'),

    path('make-order/', MakeOrderView.as_view(), name='make_order'),

    #Корзина

    path('cart/', CartView.as_view(), name='cart'),

    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),

    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),

    path('remove-from-cart-index/<str:slug>/', DeleteFromIndex.as_view(), name='delete_from_cart_index'),

    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),

    #Поиск в сайте

    path('search/', SearchResultsView.as_view(), name='search_results'),



    
    #Фильтрация

    path('filter/<int:name>/',Filters.as_view(),name='Filters'),

    # Мои заказы

    path('my_orders/',MY_ORDERS.as_view(),name='my_orders'),
    
    #коментарий
    
    path('coments/<int:pk>',base_view,name='base_product_comment'),

    path('create-comment/<int:pk>',create_comment,name='create_comment'),

    path('create-child-comment/<int:pk>',create_child_comment,name='comment_child_create'),

    #CRM
    
    #главная 

    path('index_crm',Iindex_CRM.as_view(),name='index_crm'),

    #product

    path('products_add',ProductViewCRM.as_view(),name='products_add'),
    
    #product redactor
    
    path('product_set/<str:slug>/',ProductViewCRMset.as_view(),name='product_set'),

    #product_delete

    path('product_delete/<str:slug>/',Delete_ProductCRM.as_view(),name='product_delete'),
    
    #product category

    path('ajaxcrm',AJAXCRMCategory.as_view(),name='ajaxcrm'),

    #category

    path('category_add',CategoryCRM.as_view(),name='category_add'),

    #Category redactor

    path('category_set/<str:slug>/',CategorySetCRM.as_view(),name='category_set'),

    #CATEGORY DELETE    

    path('category_delete/<str:slug>/',Delete_CategoryCRM.as_view(),name='category_delete'),



]

