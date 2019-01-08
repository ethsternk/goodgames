from django.contrib import admin
from django.urls import path
from goodgames import views
from goodgames.models import Profile, Game, Post
from goodgames import settings
from django.conf.urls.static import static

admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(Post)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="homepage"),
    path('splash/', views.splash_view),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('game/<int:game_id>', views.game_view),
    path('game/<int:game_id>/wishlist_add', views.wishlist_add_view),
    path('game/<int:game_id>/collection_add', views.collection_add_view),
    path('game/<int:game_id>/posts', views.posts_view),
    path('game/<int:game_id>/post/<int:post_id>', views.comments_view),
    path('game/<int:game_id>/reviews', views.reviews_view),
    path('profile/<int:profile_id>', views.profile_view),
    path('search/', views.search_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
