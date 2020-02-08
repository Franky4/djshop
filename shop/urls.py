from django.urls import path
# from django.conf.urls import url

from shop import views

urlpatterns = [
    path('', views.home, name='index'),
    path('search/', views.home, name='search'),
    path('sort/', views.home, name='sort'),
    path('cart_item/', views.home, name='cart_item'),
    path('orders/', views.home, name='orders'),
    path('profile/<int:pk>', views.home, name='profile'),
    path('category/', views.CategoryProduct.as_view(), name='category_list'),
    path('category-vue/', views.CategoryProductVue.as_view(), name='category_vue_list'),
    path('detail/', views.ProductDetail.as_view()),
]
