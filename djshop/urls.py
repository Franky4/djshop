from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('shop.urls')),
    # url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    path('admin/', admin.site.urls),

]