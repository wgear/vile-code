from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from person.forms import UpdateAvatarForm, RegistrationForm
from person.models import Person


def login_page(request):
    errors = []
    if request.GET.get('err') == '1':
        errors.append('Wrong username or password')

    if not request.user.is_anonymous():
        return redirect(
            reverse('home')
        )

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
    return redirect(reverse('person:login') + '?err=1')


@login_required
def out(request):
    logout(request)
    return redirect(reverse('home'))


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            person = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )

            login(request, user=person)
            return redirect(
                reverse('home')
            )
    else:
        form = RegistrationForm()

    return render(request, 'person/registration.html', {
        'form': form,
    })


def profile(request, username):
    user_profile = None
    try:
        user_profile = Person.objects.get(username=username)
    except:
        pass

    if not user_profile:
        return redirect(
            reverse('404')
        )

    is_current = request.user.pk == user_profile.pk
    is_friend = user_profile.friends.filter(id=request.user.pk).count() > 0

    return render(request, 'person/profile.html', {
        'profile': user_profile,
        'is_friend': is_friend,
        'is_current': is_current
    })


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
