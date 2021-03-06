import json
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from public.forms import CreateClubForm
from public.models import Public
from feed.models import Entry, Hashtag
from vile.service import ContentProcessor, RelatedFeeds


def create_club(request):
    if request.method == 'POST':
        form = CreateClubForm(owner=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('club:home', kwargs={'id': form.instance.pk}))
    else:
        form = CreateClubForm()
    return render(request, 'public/create.html', {
        'form': form
    })


def club_homepage(request, id):
    try:
        club = Public.objects.get(pk=id)
    except Public.DoesNotExist:
        return redirect(reverse('404'))

    is_owner = club.owner_id == request.user.pk
    is_member = club.members.filter(id=request.user.pk).count() > 0
    is_founder = club.founders.filter(id=request.user.pk).count() > 0

    is_subscribed = is_owner or is_member or is_founder

    # Get club entries
    search_hash = request.GET.get('hash', '')
    club_entries = RelatedFeeds.list(
        search_term=search_hash,
        page=request.current_page,
        club=club
    )

    # Subscribe user
    subscribe = request.GET.get('subscribe')
    if subscribe and not is_subscribed:
        is_subscribed = True
        is_member = True
        club.members.add(request.user)
        club.save()

    # Unsubscribe user
    unsubscribe = request.GET.get('unsubscribe')
    if unsubscribe and is_subscribed:
        is_subscribed = False
        is_member = False
        club.members.remove(request.user)
        club.save()

    template_name = 'public/home.html'
    if request.current_page > 1:
        template_name = 'feed/listing.html'

    return render(request,
        template_name=template_name,
        context={
            'club': club,
            'hash': search_hash,
            'entries': club_entries,
            'has_next': RelatedFeeds.has_next_page,
            'is_owner': is_owner,
            'is_member': is_member,
            'is_founder': is_founder,
            'is_subscribed': is_subscribed
        }
    )


def club_post(request, id):
    try:
        pub = Public.objects.get(pk=id)
    except Public.DoesNotExist:
        return HttpResponse(content='<p>Error</p>', content_type='text/html')
    hastags = ContentProcessor.get_hashtags(unicode(request.POST.get('content', '')))
    hastags = Hashtag.get_or_create(hastags)
    entry = Entry(content=request.POST.get('content', ''), publisher=pub, owner=request.user)
    entry.save()
    for tag in hastags:
        entry.tags.add(tag)
    entry.save()

    return render(request, 'feed/listing.html', {
        'entries': [entry]
    })
