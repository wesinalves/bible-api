from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('books', views.books, name='books'),
    path('support', views.support, name='support'),
    path('reject', views.reject, name='reject'),
    path('confirm/<int:order_id>/<str:order_secret>', views.confirm, name='confirm'),
    path('order/<int:order_id>', views.order, name='order'),


    path('versions/<str:version_abbr>', views.versions, name='versions'),
    path('search/<str:book_abbr>/<str:term>', views.search, name='searchbook'),
    path('search/<str:term>', views.search, name='search'),

    path('<str:version_abbr>/<str:book_abbr>', views.chapters, name='chapters'),
    path('<str:version_abbr>/<str:book_abbr>/<int:chapter_number>', views.verses, name='verses'),
    path('<str:version_abbr>/<str:book_abbr>/<int:chapter_number>/<int:verse_number>', views.verse, name='verse'),
    path('<str:version_abbr>/<str:book_abbr>/<int:chapter_number>/<str:verses>', views.references, name='references'),
]
