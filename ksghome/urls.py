from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('category/<slug:category_slug>/', views.posts, name='posts_by_category'),
    path('category/<slug:category_slug>/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('submit_review/<int:post_id>/', views.submit_review, name='submit_review'),
]