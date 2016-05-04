import json
from django.shortcuts import render, HttpResponse
from vile.service import RelatedFeeds
from feed.models import Hashtag


def home(request):
    return render(request, 'feed/home.html', {
        'hash': request.GET.get('hash', ''),
        'entries': RelatedFeeds.list(request.GET.get('hash'), request.GET.get('page', 1))
    })


def hashtags(request):
    search_term = request.GET.get('search', '').lower()
    qset = Hashtag.objects

    if search_term:
        qset = qset.filter(name__contains=search_term)
    qset = qset.order_by('-karma', 'name')
    return HttpResponse(
        content=json.dumps([{'text': x.name, 'value': x.pk} for x in qset.all()[:50]]),
        content_type='application/json'
    )
