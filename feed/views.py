from django.shortcuts import render
from vile.service import RelatedFeeds


def home(request):
    return render(request, 'feed/home.html', {
        'entries': RelatedFeeds.list(request.GET.get('query'), request.GET.get('page', 1))
    })
