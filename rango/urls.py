from django.urls import path, re_path

from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$',
            views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]
