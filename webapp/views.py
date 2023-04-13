from django.shortcuts import render
from .models import Version, Book, VerseVersion, Reference, Order
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import os
import json
import mercadopago
from datetime import datetime

# import operator
# from django.db.models import Q
# from functools import reduce


# Create your views here.
def index(request):
    version = request.session.get('version', 'acf')
    context = {
        'version': version,
    }
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

    if book_abbr:
        verses = VerseVersion.objects.filter(
            # version__abbreviation__iexact=version_abbr,
            verse__book__abbreviation__iexact=book_abbr,
            text__contains=term
        )
    else:
        verses = VerseVersion.objects.filter(
            version__abbreviation__iexact=version_abbr,
            text__contains=term
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
    values = [10, 20, 30, 50, 100, 200, 300]
    context = {
        'version': version,
        'values': values,
    }

    if request.method == "POST":
        api_key = os.getenv("API_KEY")
        context = {
            'version': version,
            'amount': request.POST['amount'],
            'api_key': api_key
        } 
        # order = Order.objects.create(
        #     amount=request.POST['amount']
        # )
        # order.generate_secret()
        # order.save()
        # data = {
        #     "amount": request.POST['amount'],
        #     "success_url": f"https://website.com/confirm/{order.id}/{order.secret}",
        #     "back_url": f"https://website.com/orders/{order.id}",
        # }
        # url="https://stage-api.ioka.kz/v2/orders" # trocar pela url do pagseguro
        # response = request.post(url, headers={
        #     "API-KEY": TEST_API_KEY,  # authenticate at your Provider
        #     "Content-Type": "application/json"
        # }, data=json.dumps(data))
        return render(request, 'payment.html', context=context)
       

    return render(request, 'support.html', context=context)

def process_payment(request):
    '''Process form payment'''
    token = os.getenv("ACCESS_TOKEN")
    sdk = mercadopago.SDK(token)

    request_values = request.get_json()

    payment_data = {
        "transaction_amount": float(request_values["transaction_amount"]),
        "token": request_values["token"],
        "installments": int(request_values["installments"]),
        "payment_method_id": request_values["payment_method_id"],
        "issuer_id": request_values["issuer_id"],
        "payer": {
            "email": request_values["payer"]["email"],
            "identification": {
                "type": request_values["payer"]["identification"]["type"], 
                "number": request_values["payer"]["identification"]["number"]
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    # save payment in database
    order = Order.objects.create(
        amount = float(request_values["transaction_amount"]),
        status = payment["status"],
        status_detail = payment["status_detail"],
        payment_id = payment["id"],
        date_approved = datetime.fromisoformat(payment["date_approved"]),
        payment_method = payment["payment_method_id"],
        payment_type = payment["payment_type_id"]
    )
    order.generate_secret()
    order.save()
    return HttpResponseRedirect(reverse('webapp:status_screen', args=[payment["id"]]))



def confirm(request, order_id, order_secret):
    '''Confirm the online payment.'''    
    
    order = Order.objects.get(pk=order_id)
    if order.secret == order_secret:
        order.paid = True
        order.save()
    
    return HttpResponse("OK")

def status_screen(request, payment_id):
    '''Get back order.'''
    version = request.session.get('version', 'acf')    

    context = {
        'version': version,
        'payment_id': payment_id
    }
    
    return render(request, 'status_screen.html', context=context)

def reject(request):
    '''Reject payments.'''
    version = request.session.get('version', 'acf')

    context = {
        'version': version,
    }
    
    return render(request, 'status_screen.html', context=context)