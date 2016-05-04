from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from public.forms import CreateClubForm
from public.models import Public


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
