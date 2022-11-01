from django.shortcuts import render
from .models import Version, Book

# Create your views here.
def index(request):
    return render(request, 'index.html')


def versions(request):
    """View function for version page of site."""

    versions = Version.objects.order_by('name')
    context = {
        'versions': versions,
    }

    return render(request, 'version.html', context=context)


def books(request):
    """View function for book page of site."""

    books = Book.objects.order_by('id')
    context = {
        'books': books,
    }

    return render(request, 'book.html', context=context)

