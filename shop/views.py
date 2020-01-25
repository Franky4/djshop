from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.template import loader, Context, RequestContext
from .models import Category


def home(request):
    context = {
        'menu_categoryes': Category.objects.all(),

    }
    return render(request, 'shop/base.html', context)
