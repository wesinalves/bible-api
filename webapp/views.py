from django.shortcuts import render
from .models import Version, Book, Chapter, VerseVersion

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


def chapters(request, version_abbr, book_abbr):
    """View function for chapters page of site."""
    book = Book.objects.get(        
        abbreviation=book_abbr
    )
    context = {
        'book': book,
        'range': range(1, book.chapters + 1),
        'version_abbr': version_abbr,
    }

    return render(request, 'chapters.html', context=context)


def verses(request, version_abbr, book_abbr, chapter_number):
    """View funciont to get verses."""
    verses = VerseVersion.objects.filter(
        version__abbreviation__iexact=version_abbr,
        verse__book__abbreviation__iexact=book_abbr,
        verse__chapter__number=chapter_number,
    )
    book = Book.objects.get(abbreviation=book_abbr)
    context = {
        'verses': verses,
        'version_abbr': version_abbr,
        'book': book,
        'chapter_number': chapter_number,
        'range_chapters': range(1, book.chapters + 1),
    }

    return render(request, 'verses.html', context=context)
