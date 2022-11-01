from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('versions', views.versions, name='versions'),
    path('books', views.books, name='books'),
]