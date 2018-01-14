from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page, UserProfile


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


@login_required
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


@login_required
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:

        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered}

    return render(request, 'rango/register.html', context=context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username_form')
        password = request.POST.get('password_form')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse('<strong>Your Rango account is disabled</strong>')
        else:
            print('Invalid login info: {0}, {1}'.format(username, password))
            return HttpResponse('<strong>Invalid username/password</strong>')

    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))
