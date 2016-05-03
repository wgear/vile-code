from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from public.forms import CreateClubForm


def create_club(request):
    form = CreateClubForm(owner=request.user, data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect(reverse('home'))

    return render(request, 'public/create.html', {
        'form': form
    })
