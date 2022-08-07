from rest_framework import serializers
from webapp.models import Book, Chapter, Verse, VerseVersion

class BookSerializer(serializers.HyperlinkedModelSerializer):
    """Book Serializer."""

    class Meta:
        """Meta class."""

        model = Book
        fields = ['name', 'abbreviation', 'chapters']


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    """Chapter Serializer."""
    book_name = serializers.ReadOnlyField(source='book.name')
    book_abbr = serializers.ReadOnlyField(source='book.abbreviation')
    
    class Meta:
        """Meta class."""

        model = Chapter        
        fields = ['book_name', 'book_abbr', 'number', 'verses']


class VerseSerializer(serializers.ModelSerializer):
    """Verse Serializer."""
    book_abbr = serializers.ReadOnlyField(source='book.abbreviation')

    class Meta:
        """Meta class."""

        model = Verse
        fields = ['book_abbr', 'chapter', 'number',
                    'versions', 'dictionaries', 'intelinears']


class VerseVersionSerializer(serializers.ModelSerializer):
    """Verse Version Serializer."""
    book_abbr = serializers.ReadOnlyField(source='verse.book.abbreviation')
    chapter_number = serializers.ReadOnlyField(source='verse.chapter.number')
    verse_number = serializers.ReadOnlyField(source='verse.number')
    version_abbr = serializers.ReadOnlyField(source='version.abbreviation')

    class Meta:
        """Meta class."""

        model = VerseVersion
        fields = [
            'id',
            'book_abbr',
            'chapter_number',
            'verse_number',
            'verse',
            'version_abbr',
            'text'
        ]

