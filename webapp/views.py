from django.shortcuts import render
from .models import Version, Book, VerseVersion, Reference, Order
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse


import os
import stripe
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
        stripe.api_key = 'sk_test_Ho24N7La5CVDtbmpjc377lJI'
        # price = request.POST["amount"]
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': '{{price_id}}',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=reverse('success'),
                cancel_url=reverse('cancel')
            )        
            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            return HttpResponse(e)       

    return render(request, 'support.html', context=context)

# def process_payment(request):
#     '''Process form payment'''
#     token = os.getenv("ACCESS_TOKEN")
#     sdk = mercadopago.SDK(f"{token}")

#     #return HttpResponse(request)
#     data = json.loads(request.body)    

#     payment_data = {
#         "transaction_amount": float(data["transaction_amount"]),
#         #"token": data["token"],
#         #"installments": int(data["installments"]),
#         "payment_method_id": data["payment_method_id"],
#         "description": "Doação para o site Bibliamax",        
#         "payer": {
#             "email": data["payer"]["email"],
#             "identification": {
#                 "type": data["payer"]["identification"]["type"],
#                 "number": data["payer"]["identification"]["number"]
#             },            
#         }
#     }

#     payment_response = sdk.payment().create(payment_data)
#     payment = payment_response["response"]    

#     # save payment in database
#     order = Order.objects.create(
#         amount = float(data["transaction_amount"]),
#         status = payment["status"],
#         status_detail = payment["status_detail"],
#         payment_id = payment["id"],
#         date_approved = datetime.fromisoformat(payment["date_approved"]),
#         payment_method = payment["payment_method_id"],
#         payment_type = payment["payment_type_id"]
#     )
#     order.generate_secret()
#     order.save()
#     return HttpResponseRedirect(reverse('status', args=[payment["id"]]))
#     #return HttpResponse("OK")
#     # response = {
#     #     "status": "ok",
#     #     "data": {
#     #         "redirect": reverse('status', args=[payment["id"]]),            
#     #     }
#     # }
#     # return HttpResponse(json.dumps(response), content_type='application/json')



def confirm(request, order_id, order_secret):
    '''Confirm the online payment.'''    
    
    order = Order.objects.get(pk=order_id)
    if order.secret == order_secret:
        order.paid = True
        order.save()
    
    return HttpResponse("OK")

def success(request, payment_id):
    '''Get back order.'''
    version = request.session.get('version', 'acf')    

    context = {
        'version': version,
        'payment_id': payment_id
    }
    
    return render(request, 'success.html', context=context)

def reject(request):
    '''Reject payments.'''
    version = request.session.get('version', 'acf')

    context = {
        'version': version,
    }
    
    return render(request, 'status_screen.html', context=context)