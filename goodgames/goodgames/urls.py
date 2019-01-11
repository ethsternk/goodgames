from django.contrib import admin
from django.urls import path
from goodgames import views
from goodgames.models import Profile, Game, Post, Comment, Review
from django.conf import settings
from django.conf.urls.static import static

admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Review)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeView.as_view(), name="homepage"),
    path('splash/', views.splash_view),
    path('login/', views.loginView.as_view()),
    path('signup/', views.signupView.as_view()),
    path('logout/', views.logout_view),
    path('game/<int:game_id>', views.game_view),
    path('game/<int:game_id>/wishlist_add', views.wishlist_add_view),
    path('game/<int:game_id>/collection_add', views.collection_add_view),
    path('game/<int:game_id>/wishlist_remove', views.wishlist_remove_view),
    path('game/<int:game_id>/collection_remove', views.collection_remove_view),
    path('game/<int:game_id>/posts', views.posts_view),
    path('game/<int:game_id>/post/<int:post_id>', views.comments_view),
    path('game/<int:game_id>/reviews', views.reviews_view),
    path('profile/<int:profile_id>', views.profile_view),
    path('search/', views.search_view),
    path('all-posts/', views.all_posts_view),
    path('all-reviews/', views.all_reviews_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'goodgames.views.handler404'
handler500 = 'goodgames.views.handler500'
