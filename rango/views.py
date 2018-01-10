from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': pages_list}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'myname': 'YG'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = dict()

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', context={'form': form})


def add_page(request, category_name_slug):
    form = PageForm()
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        if category:
            form = PageForm(request.POST)

            if form.is_valid():
                page = form.save(commit=False)
                page.category = category
                page.save()

                return HttpResponseRedirect(reverse('rango:show_category', args=(category_name_slug,)))
            else:
                print(form.errors)

    context_dict = dict()
    context_dict['category'] = category
    context_dict['form'] = form
    return render(request, 'rango/add_page.html', context=context_dict)
