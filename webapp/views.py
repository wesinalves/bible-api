from django.shortcuts import render
from .models import Version, Book, VerseVersion, Reference, Order
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from openai import OpenAI


import os
import stripe
from datetime import datetime

# import operator
# from django.db.models import Q
# from functools import reduce


# Create your views here.
def index(request):
    version = request.session.get('version', 'nvi')
    context = {
        'version': version,
    }
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        print(response)
        return JsonResponse({'response': response})
    return render(request, 'index.html', context=context)


def versions(request, version_abbr='acf'):
    """View function for version page of site."""

    request.session['version'] = version_abbr
    changed = False
    if request.session['version'] != version_abbr:
        changed = True
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

    book = Book.objects.get(
        abbreviation=book_abbr
    )
    context = {
        'book': book,
        'range': range(1, book.chapters + 1),
        'version': version_abbr,
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
    books = Book.objects.all()
    versions = Version.objects.order_by('name')
    context = {
        'verses': verses,
        'version': version_abbr,
        'versions': versions,
        'book': book,
        'books': books,
        'chapter_number': chapter_number,
        'range_chapters': range(1, book.chapters + 1),
    }

    return render(request, 'verses.html', context=context)


def verse(request, version_abbr, book_abbr, chapter_number, verse_number):
    """View funciont to get verses."""

    verse = VerseVersion.objects.get(
        version__abbreviation__iexact=version_abbr,
        verse__book__abbreviation__iexact=book_abbr,
        verse__chapter__number=chapter_number,
        verse__number=verse_number
    )
    book = Book.objects.get(abbreviation=book_abbr)
    books = Book.objects.all()
    dictionaries = verse.verse.dictionaries.all()
    inters = verse.verse.intelinears.all()
    references = Reference.objects.filter(reference=verse.verse.id)
    # image = get_image("terra sem forma e vazia")
    context = {
        'verse': verse,
        'version': version_abbr,
        'book': book,
        'books': books,
        'references': references,
        'dictionaries': dictionaries,
        'inters': inters,
        'chapter_number': chapter_number,
        'range_chapters': range(1, book.chapters + 1),
        # 'image': image,
    }

    return render(request, 'verse.html', context=context)


def references(request, version_abbr, book_abbr, chapter_number, verses):
    """View funciont to get verses."""
    verses_list = verses.split(",")

    verses = VerseVersion.objects.filter(
        version__abbreviation__iexact=version_abbr,
        verse__book__abbreviation__iexact=book_abbr,
        verse__chapter__number=chapter_number,
        verse__number__in=verses_list
    )
    book = Book.objects.get(abbreviation=book_abbr)
    books = Book.objects.all()
    context = {
        'verses': verses,
        'version': version_abbr,
        'book': book,
        'books': books,
        'chapter_number': chapter_number,
        'range_chapters': range(1, book.chapters + 1),
    }

    return render(request, 'verses.html', context=context)


def search(request, term, book_abbr=None):
    """View function to search verses."""

    version_abbr = request.session.get('version', 'acf')
    verses = VerseVersion.objects.filter(
        version__abbreviation__iexact=version_abbr,
        text__icontains=term
    )

    if book_abbr:
        verses = verses.filter(
            verse__book__abbreviation__iexact=book_abbr,
        )
    # verses = VerseVersion.objects.filter(
    #         reduce(
    #             operator.and_, (
    #                 Q(
    #                     version__abbreviation__iexact=version_abbr,
    #                     text__icontains=x
    #                 ) for x in term)
    #         )

    #     )

    books = Book.objects.all()
    context = {
        'verses': verses,
        'version': version_abbr,
        'books': books,
        'term': term,
    }

    return render(request, 'search.html', context=context)


def terms(request):
    '''View function to terms of usage.'''

    version = request.session.get('version', 'acf')
    context = {
        'version': version,
    }

    return render(request, 'terms.html', context=context)


def privacy(request):
    '''View function to privacy policy.'''

    version = request.session.get('version', 'acf')
    context = {
        'version': version,
    }

    return render(request, 'policy.html', context=context)


def support(request):
    '''View function to privacy policy.'''

    version = request.session.get('version', 'acf')
    quantities = [1, 2, 3, 4, 7, 10]
    context = {
        'version': version,
        'values': quantities,
    }

    if request.method == "POST":
        stripe.api_key = os.getenv("API_KEY")
        quantity = request.POST["quantity"]
        try:
            # stripe checkout
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': os.getenv("PRICE_ID"),
                        'quantity': quantity,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel'))
            )
            # save payment in database
            order = Order.objects.create(
                amount=float(request.POST["quantity"]) * 30,
                status="approved",
                date_approved=datetime.now(),
                payment_method="credit card",
                payment_type="payment"
            )
            order.generate_secret()
            order.save()
            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            return HttpResponse(e)

    return render(request, 'support.html', context=context)


def success(request):
    '''Get back order.'''
    version = request.session.get('version', 'acf')

    context = {
        'version': version,
    }

    return render(request, 'success.html', context=context)


def cancel(request):
    '''Reject payments.'''
    version = request.session.get('version', 'acf')

    context = {
        'version': version,
    }

    return render(request, 'cancel.html', context=context)


def get_completion(prompt):
    '''Chat with the bot.'''
    chatbot = OpenAI()
    completion = chatbot.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um teólogo que domina a bíblia da Nova Versão Internacional, você vai fornecer textos da bíblia, comentários bíblicos, reflexões baseadas na bíblia, resumo de capítulos da bíblia, mensagens de motivacionais baseadas na bíblia, mensagens de conforto e esperança baseadas na bíblia.'"},
            {"role": "system", "content": "Se por acaso for pedido um texto muito grande da bíblia, exemplo salmo 119, não justifique o porque não pode trazer um texto tão grande, apenas escreva o máximo que puder, e quando não puder mais, escreva um sinal de continuação no final"},
            {"role": "system", "content": "Escreva o texto separado por versículos, e enumere cada um"},
            {"role": "user", "content": prompt},
        ]
    )

    response = completion.choices[0].message.content
    return response


def get_image(prompt):
    dalle = OpenAI()
    response = dalle.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url
