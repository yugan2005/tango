from django.urls import path, re_path

from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$',
            views.show_category, name='show_category'),
]