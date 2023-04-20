from django.db import models
import random


class Idiom(models.Model):
    """Idiom class."""

    name = models.CharField(max_length=100)
    native_name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return the name of the Idiom."""
        return self.name


class Version(models.Model):
    """Version Class."""

    idiom = models.ForeignKey(Idiom, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=20)
    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return the name of the version."""
        return self.name


class Book(models.Model):
    """Book Class."""

    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=5)
    chapters = models.IntegerField(default=0)
    versions = models.ManyToManyField(Version, through='BookVersion')

    def __str__(self) -> str:
        """Return the name of the book."""
        return self.name


class BookVersion(models.Model):
    """Book Version realtionship."""

    name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return the name of the book version."""
        return self.name


class Chapter(models.Model):
    """Chapter Class."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.IntegerField()
    verses = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Return the number of the chapter."""
        return f"{self.book.name} cap. {self.number}"


class Interlinear(models.Model):
    """Interlinear Class."""

    strong = models.CharField(max_length=100)
    definition = models.TextField()
    origin = models.TextField()
    use = models.TextField()
    classification = models.TextField()
    transcription = models.CharField(max_length=200)
    pronounce = models.CharField(max_length=200)
    spelling = models.CharField(max_length=200)

    def __str__(self) -> str:
        """Return the reference."""
        return self.definition


class Dictionary(models.Model):
    """Dictionary Class."""

    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self) -> str:
        """Return the dictionary."""
        return self.title


class Verse(models.Model):
    """Verse Class."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    number = models.IntegerField()
    versions = models.ManyToManyField(Version, through='VerseVersion')
    dictionaries = models.ManyToManyField(Dictionary, through='VerseDictionary', blank=True)
    intelinears = models.ManyToManyField(Interlinear, through='VerseInterlinear', blank=True)

    def __str__(self) -> str:
        """Return the number of the verse."""
        return f"{self.book.abbreviation} {self.chapter.number}:{self.number}"


class VerseInterlinear(models.Model):
    """Verse Interlinear Relationship."""

    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    interlinear = models.ForeignKey(Interlinear, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return the number of the verse."""
        return f'{self.verse.book.abbreviation} {self.verse.chapter.number}:{self.verse.number}'


class VerseDictionary(models.Model):
    """Verse Dicitionary Relationship."""

    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return the number of the verse."""
        return f'{self.verse.book.abbreviation} {self.verse.chapter.number}:{self.verse.number}'


class VerseVersion(models.Model):
    """Verse Version Relationship."""

    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        """Return the number of the verse."""
        return f'{self.verse.book.abbreviation} {self.verse.chapter.number}:{self.verse.number}'


class Reference(models.Model):
    """Reference Class."""

    reference = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name='verse_fk')
    text = models.CharField(max_length=100)
    book = models.CharField(max_length=5)
    chapter = models.IntegerField()
    verse = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return the reference."""
        return self.text

class Order(models.Model):
    secret = models.CharField(max_length=1000, default="", blank=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=10, default="")
    date_approved = models.DateTimeField()
    payment_method = models.CharField(max_length=100, default="", blank=True)
    payment_type = models.CharField(max_length=100, default="", blank=True)

    def __str__(self) -> str:
        """Return the order chekout"""
        return str(self.secret)
    
    def generate_secret(self):
        self.secret = str(random.randint(10000, 99999))