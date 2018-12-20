from django.shortcuts import render, HttpResponseRedirect, reverse
from goodgames.models import Profile, Game
from goodgames.forms import SignupForm, LoginForm, SearchForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import requests
# from django.contrib.auth.decorators import login_required


def home_view(request):
    user = None
    if request.user.username:
        user = Profile.objects.filter(user=request.user).first()
    form = SearchForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        results = requests.get(
            'https://api-endpoint.igdb.com/games/?search=' +
            data['search'] + '&fields=id,name,cover',
            headers={
                'user-key': '28db14f003075ce68766bfe55e7e9279',
                'accept': 'application/json',
            }
        ).json()
        return render(request, 'search.html', {
            'data': {'results': results},
            'form': form,
        })
    popular = requests.get(
        'https://api-endpoint.igdb.com/games/'
        '?fields=id,name,cover,popularity&order=popularity:desc',
        headers={
            'user-key': '28db14f003075ce68766bfe55e7e9279',
            'accept': 'application/json',
        }
    ).json()
    print(popular[0])
    return render(request, 'home.html', {
        'data': {
            'user': user,
            'popular': popular,
        },
        'form': form,
    })


def game_view(request, game_id):
    user = None
    if request.user.username:
        user = Profile.objects.filter(user=request.user).first()
    game = requests.get(
        "https://api-endpoint.igdb.com/games/" + str(game_id),
        headers={
            'user-key': '28db14f003075ce68766bfe55e7e9279',
            'accept': 'application/json',
        }
    ).json()[0]
    # related = []
    # for item in game['games']:
    #     related.append(requests.get(
    #         "https://api-endpoint.igdb.com/games/" + str(item),
    #         headers={
    #             'user-key': '28db14f003075ce68766bfe55e7e9279',
    #             'accept': 'application/json',
    #         }
    #     ).json()[0])
    return render(request, 'game.html', {'data': {
        'game': game,
        'user': user,
        # 'related': related,
    }})


def profile_view(request, profile_id):
    user = None
    user_wish = None
    user_coll = None
    if request.user.username:
        user = Profile.objects.filter(user=request.user).first()
        user_wish = user.wishlist.all()
        user_coll = user.collection.all()
    profile = Profile.objects.filter(id=profile_id).first()
    profile_wish = profile.wishlist.all()
    profile_coll = profile.collection.all()
    return render(request, 'profile.html', {'data': {
        'profile': profile,
        'wishlist': profile_wish,
        'collection': profile_coll,
        'user': user,
        'give': [game for game in profile_wish if game in user_coll],
        'take': [game for game in profile_coll if game in user_wish],
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


def wishlist_add_view(request, game_id):
    user = Profile.objects.filter(user=request.user).first()
    if Game.objects.filter(igdb_id=game_id):
        user.wishlist.add(Game.objects.filter(igdb_id=game_id).first())
    else:
        game = requests.get(
            "https://api-endpoint.igdb.com/games/" + str(game_id),
            headers={
                'user-key': '28db14f003075ce68766bfe55e7e9279',
                'accept': 'application/json',
            }
        ).json()[0]
        new_game = Game.objects.create(
            igdb_id=game_id,
            name=game['name'],
            cover=game['cover']['cloudinary_id'],
        )
        user.wishlist.add(new_game)
    return HttpResponseRedirect('/profile/' + str(user.id))


def collection_add_view(request, game_id):
    user = Profile.objects.filter(user=request.user).first()
    if Game.objects.filter(igdb_id=game_id):
        user.collection.add(Game.objects.filter(igdb_id=game_id).first())
    else:
        game = requests.get(
            "https://api-endpoint.igdb.com/games/" + str(game_id),
            headers={
                'user-key': '28db14f003075ce68766bfe55e7e9279',
                'accept': 'application/json',
            }
        ).json()[0]
        new_game = Game.objects.create(
            igdb_id=game_id,
            name=game['name'],
            cover=game['cover']['cloudinary_id'],
        )
        user.collection.add(new_game)
    return HttpResponseRedirect('/profile/' + str(user.id))


def search_view(request):
    form = SearchForm(None or request.POST)
    results = None
    if form.is_valid():
        data = form.cleaned_data
        results = requests.get(
            'https://api-endpoint.igdb.com/games/?search=' +
            data['search'] + '&fields=id,name,cover',
            headers={
                'user-key': '28db14f003075ce68766bfe55e7e9279',
                'accept': 'application/json',
            }
        ).json()
    return render(request, 'search.html', {
        'data': {'results': results},
        'form': form,
    })
