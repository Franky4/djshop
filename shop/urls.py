from django.urls import path
# from django.conf.urls import url

from shop import views

urlpatterns = [
    path('', views.home, name='index'),
    path('search', views.home, name='search')
]
