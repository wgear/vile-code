import json
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from public.forms import CreateClubForm
from public.models import Public
from feed.models import Entry


def create_club(request):
    if request.method == 'POST':
        form = CreateClubForm(owner=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = CreateClubForm()
    return render(request, 'public/create.html', {
        'form': form
    })


def club_homepage(request, id):
    try:
        pub = Public.objects.get(pk=id)
    except Public.DoesNotExist:
        return redirect(reverse('home'))

    return render(request, 'public/home.html', {
        'club': pub
    })


def club_post(request, id):
    try:
        pub = Public.objects.get(pk=id)
    except Public.DoesNotExist:
        return HttpResponse(content='<p>Error</p>', content_type='text/html')
    hastags = Entry.detect_hashtags(request.POST.get('content', ''))
    entry = Entry(content=request.POST.get('content', ''), publisher=pub)
    entry.save()
    for tag in hastags:
        entry.tags.add(tag)
    entry.save()

    return render(request, 'feed/listing.html', {
        'entries': [entry]
    })
