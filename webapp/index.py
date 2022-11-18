import algoliasearch_django as algoliasearch

from .models import Book, Version, Idiom, VerseVersion

algoliasearch.register(Book)
algoliasearch.register(Version)
algoliasearch.register(Idiom)
algoliasearch.register(VerseVersion)
