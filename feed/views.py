import json
from django.shortcuts import render, HttpResponse
from vile.service import RelatedFeeds
from feed import models as feed_models
from person import models as person_models
from public import models as public_models


def home(request):
    return render(request, 'feed/home.html', {
        'hash': request.GET.get('hash', ''),
        'entries': RelatedFeeds.list(request.GET.get('hash'), request.GET.get('page', 1))
    })


def hashtags(request):
    search_term = request.GET.get('search', '').lower()
    qset = feed_models.Hashtag.objects

    if search_term:
        qset = qset.filter(name__contains=search_term)
    qset = qset.order_by('-karma', 'name')
    return HttpResponse(
        content=json.dumps([{'text': x.name, 'value': x.pk} for x in qset.all()[:50]]),
        content_type='application/json'
    )


def vote(request):
    if request.method != 'POST':
        return HttpResponse(content='-', content_type='text/plain')

    available = [
        feed_models,
        person_models,
        public_models
    ]

    target = request.POST.get('to', '.').split('.')
    target_model = target[0]
    target_pk = target[1]

    positive = int(request.POST.get('positive', '1')) > 0

    model_instance = None
    for mdl in available:
        if hasattr(mdl, target_model):
            model_instance = getattr(mdl, target_model)
        break

    if model_instance is None:
        return HttpResponse(content='-', content_type='text/plain')

    try:
        instance = model_instance.objects.get(pk=int(target_pk))
    except:
        return HttpResponse(content='-', content_type='text/plain')

    instance.vote(author=request.user, positive=positive)
    return HttpResponse(content=str(instance.karma), content_type='text/plain')
