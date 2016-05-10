import json
from feed.forms import CommentForm
from vile.service import RelatedFeeds
from feed import models as feed_models
from person import models as person_models
from public import models as public_models
from public.views import club_homepage
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, redirect


def handle_public_home(request):
    if not request.subdomain:
        return

    public = public_models.Public.objects.filter(slug__iexact=request.subdomain).first()
    if not public:
        return

    return club_homepage(request, public.pk)


def home(request):
    public = handle_public_home(request)
    if public is not None:
        return public

    entries = RelatedFeeds.list(
        search_term=request.GET.get('hash', ''),
        page=request.current_page
    )

    template_name = 'feed/home.html'
    if request.current_page > 1:
        template_name = 'feed/listing.html'

    return render(request, template_name, {
        'hash': request.GET.get('hash', ''),
        'entries': entries,
        'has_next': RelatedFeeds.has_next_page
    })


def entry_detail(request, id):
    try:
        entry = feed_models.Entry.objects.get(pk=id)
    except feed_models.Entry.DoesNotExist:
        return redirect(reverse('404'))

    club = entry.publisher
    is_owner = club.owner_id == request.user.pk
    is_member = club.members.filter(id=request.user.pk).count() > 0
    is_founder = club.founders.filter(id=request.user.pk).count() > 0

    is_subscribed = is_owner or is_member or is_founder

    return render(request, 'feed/entry.html', {
        'entry': entry,
        'club': club,
        'is_owner': is_owner,
        'is_member': is_member,
        'is_founder': is_founder,
        'is_subscribed': is_subscribed
    })


def hashtags(request):
    search_term = request.GET.get('search', '').lower()
    qset = feed_models.Hashtag.objects

    if search_term:
        qset = qset.filter(name__contains=search_term)
    qset = qset.order_by('-karma', 'name')
    return HttpResponse(
        content=json.dumps([{'text': '#' + x.name, 'value': x.pk} for x in qset.all()[:50]]),
        content_type='application/json'
    )


def comment(request):
    if request.method != 'POST':
        return HttpResponse(content='', content_type='text/html')

    form = CommentForm(author=request.user, data=request.POST.copy())
    if form.is_valid():
        form.save()
        return render(request, 'feed/comment_detail.html', {
            'comment': form.instance
        })

    return HttpResponse(content_type='text/html')


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
