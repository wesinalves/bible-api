from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),    
    path('versions/<str:version_abbr>', views.versions, name='versions'),
    path('books', views.books, name='books'),
    path('<str:version_abbr>/<str:book_abbr>', views.chapters, name='chapters'),
    path('<str:version_abbr>/<str:book_abbr>/<int:chapter_number>', views.verses, name='verses'),
]