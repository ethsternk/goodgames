from django.shortcuts import render, HttpResponseRedirect, reverse
from goodgames.models import Profile, Game, Post, Comment, Review
from goodgames.forms import (
    SignupForm, LoginForm, PostForm, SearchForm, CommentForm, ReviewForm)
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import requests
from datetime import datetime
from django.db.models import Avg


def splash_view(request):
    if request.user.username:
        return HttpResponseRedirect(reverse('homepage'))
    else:
        return render(request, 'splash.html')


def home_view(request):
    user = request.user.profile if request.user.is_authenticated else None
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
    top1 = popular[0:4]
    top2 = popular[5:9]
    return render(request, 'home.html', {
        'data': {
            'user': user,
            'top1': top1,
            'top2': top2
        },
        'form': form,
    })


def game_view(request, game_id):
    user = request.user.profile if request.user.is_authenticated else None
    game = requests.get(
        "https://api-endpoint.igdb.com/games/" + str(game_id),
        headers={
            'user-key': '28db14f003075ce68766bfe55e7e9279',
            'accept': 'application/json',
        }
    ).json()[0]
    game_instance = Game.objects.filter(igdb_id=game_id).first()
    reviews = Review.objects.filter(game=game_instance)
    score = reviews.aggregate(Avg('score'))
    score = "%.1f" % score['score__avg']
    return render(request, 'game.html', {
        'data': {
            'game': game,
            'user': user,
            'score': score,
        }
    })


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
    posts = Post.objects.filter(profile=profile)
    return render(request, 'profile.html', {'data': {
        'profile': profile,
        'wishlist': profile_wish,
        'collection': profile_coll,
        'user': user,
        'give': [game for game in profile_wish if game in user_coll],
        'take': [game for game in profile_coll if game in user_wish],
        'posts': posts,
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


def posts_view(request, game_id):
    game = Game.objects.filter(igdb_id=game_id).first()
    user = request.user.profile if request.user.is_authenticated else None
    posts = Post.objects.filter(game=game)
    form = PostForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            if not game:
                game = Game.objects.create(
                    igdb_id=game_id,
                    name=game['name'],
                    cover=game['cover']['cloudinary_id'],
                )
            data = form.cleaned_data
            Post.objects.create(
                title=data['title'],
                body=data['body'],
                game=game,
                date=datetime.now(),
                profile=request.user.profile,
            )
            return HttpResponseRedirect('/game/' + str(game_id) + '/posts')
    return render(request, 'game_posts.html', {
        'data': {
            'game': game,
            'user': user,
            'posts': posts,
        },
        'form': form,
    })


def comments_view(request, game_id, post_id):
    game = Game.objects.filter(igdb_id=game_id).first()
    post = Post.objects.filter(id=post_id).first()
    comments = Comment.objects.filter(post=post)
    form = CommentForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(
                body=data['body'],
                post=post,
                date=datetime.now(),
                profile=request.user.profile,
            )
            return HttpResponseRedirect(
                '/game/' + str(game_id) + '/post/' + str(post_id))
    return render(request, 'post.html', {
        'data': {
            'game': game,
            'user': request.user.profile,
            'post': post,
            'comments': comments,
        },
        'form': form,
    })


def reviews_view(request, game_id):
    game = Game.objects.filter(igdb_id=game_id).first()
    user = request.user.profile if request.user.is_authenticated else None
    reviews = Review.objects.filter(game=game)
    form = ReviewForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            if not game:
                game = Game.objects.create(
                    igdb_id=game_id,
                    name=game['name'],
                    cover=game['cover']['cloudinary_id'],
                )
            data = form.cleaned_data
            Review.objects.create(
                title=data['title'],
                body=data['body'],
                score=data['score'],
                game=game,
                date=datetime.now(),
                profile=request.user.profile,
            )
            return HttpResponseRedirect('/game/' + str(game_id) + '/reviews')
    return render(request, 'reviews.html', {
        'data': {
            'game': game,
            'user': user,
            'reviews': reviews,
        },
        'form': form,
    })
