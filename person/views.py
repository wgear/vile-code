from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from person.forms import UpdateAvatarForm


def login_page(request):
    errors = []
    if request.GET.get('err') == '1':
        errors.append('Wrong username or password')

    return render(request, 'person/login.html', {
        'message': errors
    })


def authorize(request):
    user = authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )

    if user is not None and user.is_active:
        login(request, user)
        return redirect(reverse('home'))
    return redirect(reverse('login') + '?err=1')


def out(request):
    logout(request)
    return redirect(reverse('home'))


def avatar(request):
    if request.method == 'POST':
        form = UpdateAvatarForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect(reverse('person:avatar'))
    form = UpdateAvatarForm()
    return render(request, 'person/change_avatar.html', {
        'form': form
    })
