import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()

import random

from rango.models import Category, Page


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/2/tutorial/'},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorial/python/'}]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/1.9/intro/tutorial01/'},
        {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/'}]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org'}]

    python_user_groups_pages = [
        {'title': 'Google group',
         'url': 'http://www.google.com'},
        {'title': 'Facebook group',
         'url': 'http://www.facebook.com'},
        {'title': 'LinkedIn group',
         'url': 'http://www.linkedin.com'}
    ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16},
            'Python user groups': {'pages': python_user_groups_pages, 'views': 16, 'likes': 8}}

    rand_seed = 1
    random.seed(rand_seed)

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], random.randint(0, 100))

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


if __name__ == '__main__':
    print('Starting Rango population script ...')
    populate()
