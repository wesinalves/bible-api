from webapp.models import Book, Chapter, Verse, VerseVersion
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import BookSerializer, \
    ChapterSerializer, VerseSerializer, VerseVersionSerializer
from django.db.models import Q



class BookViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Books to be viewed or edited."""

    queryset = Book.objects.all().order_by('-name')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChapterViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Chapters to be viewed or edited."""

    queryset = Chapter.objects.all().order_by('-id')
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]


class VerseViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Verses to be viewed or edited."""

    queryset = Verse.objects.all().order_by('-id')
    serializer_class = VerseSerializer
    permission_classes = [permissions.IsAuthenticated]


class VerseVersionViewSet(viewsets.ModelViewSet):
    """Api endpoint that allows verses to be viewed."""

    queryset = VerseVersion.objects.all().order_by('id')
    serializer_class = VerseVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        version = self.kwargs.get("version", None)
        book = self.kwargs.get("book", None)
        chapter = self.kwargs.get("chapter", None)
        verse = self.kwargs.get("verse", None)
        print(version, book, chapter, verse)
        if version is not None and book is not None and chapter is not None and verse is not None:
            return VerseVersion.objects.filter(
                version__abbreviation__iexact=version,
                verse__book__abbreviation__iexact=book,
                verse__chapter__number=chapter,
                verse__number=verse,
            )
        elif version is not None and book is not None and chapter is not None:
            return VerseVersion.objects.filter(
                version__abbreviation__iexact=version,
                verse__book__abbreviation__iexact=book,
                verse__chapter__number=chapter
            )
        elif version is not None and book is not None:
            return VerseVersion.objects.filter(
                version__abbreviation__iexact=version,
                verse__book__abbreviation__iexact=book
            )

        return super().get_queryset()
