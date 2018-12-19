from django.shortcuts import render, HttpResponseRedirect, reverse
from goodgames.models import Profile
from goodgames.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required


def home_view(request):
    profile = None
    if request.user.username:
        profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'home.html', {'data': {
        'profile': profile,
    }})


def signup_view(request):
    html = 'signup.html'
    form = SignupForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        Profile.objects.create(
            name=user.username,
            user=user,
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, html, {'form': form})


def login_view(request):
    html = 'login.html'
    form = LoginForm(None or request.POST)
    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(
            username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('homepage'))
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
