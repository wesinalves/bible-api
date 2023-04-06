from django.contrib import admin

# Register your models here.
from .models import Idiom, Book, BookVersion, Chapter, \
Verse, VerseVersion, VerseDictionary, VerseInterlinear, \
Reference, Interlinear, Dictionary, Version, Order


class BookVersionAdmin(admin.StackedInline):
    """BookVersion Inline."""

    model = BookVersion
    extra = 1


class InterlinearAdmin(admin.StackedInline):
    """BookVersion Inline."""

    model = VerseInterlinear
    extra = 1


class DictionaryAdmin(admin.StackedInline):
    """BookVersion Inline."""

    model = VerseDictionary
    extra = 1


class ReferenceAdmin(admin.StackedInline):
    """BookVersion Inline."""

    model = Reference
    extra = 1
    fk_name = 'reference'


class BookAdmin(admin.ModelAdmin):
    """Book Admin."""

    search_fields = ['name']
    inlines = [
        BookVersionAdmin,
    ]


class VerseAdmin(admin.ModelAdmin):
    """Verse Admin."""

    list_filter = ['book']
    list_display = ['number', 'chapter']
    search_fields = ['book', 'chapter', 'number']
    inlines = [
        DictionaryAdmin, InterlinearAdmin, ReferenceAdmin
    ]


class VerseVersionAdmin(admin.ModelAdmin):
    """BookVersion Inline."""

    list_filter = ['version']
    list_display = ['verse', 'version']
    search_fields = ['verse', 'version', 'text']
    readonly_fields = ['verse', 'version']


class VersionAdmin(admin.ModelAdmin):
    """Version Admin."""

    list_display = ['name', 'abbreviation']


admin.site.register(Idiom)
admin.site.register(Version, VersionAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter)
admin.site.register(Verse, VerseAdmin)
admin.site.register(Interlinear)
admin.site.register(Dictionary)
admin.site.register(VerseVersion, VerseVersionAdmin)
admin.site.register(Order)

# sMw%SQzO$ziJ 0 O
