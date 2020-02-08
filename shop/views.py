from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader, Context, RequestContext
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Category, Product, Cart, CartItem, Order
from .serializers import CatSer, ProductSer


def home(request):
    context = {
        'menu_categoryes': Category.objects.all(),
        'object_list': Product.objects.all(),

    }
    return render(request, 'shop/base.html', context)


class ProductDetail(DetailView):
    """Карточка товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartItemForm()
        return context


class CategoryProduct(ListView):
    """Список товаров из категории"""
    template_name = 'shop/list-product.html'
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])
        return products


class CategoryProductVue(View):
    """Список товаров из категории для vue"""
    def get(self, request):
        return render(request, 'shop/vue/list-product-vue.html')

    def post(self, request):
        slug = request.POST.get('slug')
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])

        category_ser = CatSer(Category.objects.filter(parent__isnull=True), many=True)
        serializers = ProductSer(products, many=True)
        return JsonResponse(
            {
                'products': serializers.data,
                'category': category_ser.data
            },
            safe=False
        )
