from django.shortcuts import render
from .models import Version, Book, Chapter, VerseVersion

# Create your views here.
def index(request):
    version = request.session.get('version', 'acf')
    context = {
        'version': version,
    }
    return render(request, 'index.html', context=context)


def versions(request, version_abbr='acf'):
    """View function for version page of site."""    

    changed = False
    if request.session['version'] != version_abbr:
        changed = True
    request.session['version'] = version_abbr
    version = request.session['version']
    versions = Version.objects.order_by('name')
    context = {
        'versions': versions,
        'version': version,
        'changed': changed,
    }

    return render(request, 'version.html', context=context)


def books(request):
    """View function for book page of site."""

    version = request.session.get('version', 'acf')
    books = Book.objects.order_by('id')
    context = {
        'books': books,
        'version': version,
    }

    return render(request, 'book.html', context=context)


def chapters(request, version_abbr, book_abbr):
    """View function for chapters page of site."""

    version = request.session.get('version', 'acf')
    book = Book.objects.get(        
        abbreviation=book_abbr
    )
    context = {
        'book': book,
        'range': range(1, book.chapters + 1),
        'version_abbr': version_abbr,
        'version': version,
    }

    return render(request, 'chapters.html', context=context)


def verses(request, version_abbr, book_abbr, chapter_number):
    """View funciont to get verses."""

    version = request.session.get('version', 'acf')
    verses = VerseVersion.objects.filter(
        version__abbreviation__iexact=version_abbr,
        verse__book__abbreviation__iexact=book_abbr,
        verse__chapter__number=chapter_number,
    )
    book = Book.objects.get(abbreviation=book_abbr)
    books = Book.objects.all()
    context = {
        'verses': verses,
        'version_abbr': version_abbr,
        'book': book,
        'books': books,
        'chapter_number': chapter_number,
        'range_chapters': range(1, book.chapters + 1),
        'version': version,
    }

    return render(request, 'verses.html', context=context)
