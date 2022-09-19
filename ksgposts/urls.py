from django.urls import path
from ksghome import views


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('category/<slug:category_slug>/', views.posts, name='posts_by_category'),
    path('category/<slug:category_slug>/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
] 
