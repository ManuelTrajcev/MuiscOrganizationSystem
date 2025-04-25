from django.urls import path
from . import views

urlpatterns = [
    path('album/', views.album_list, name='album_list'),
    path('artist/', views.artist_list, name='artist_list'),
    path('track/', views.track_list, name='track_list'),
    path('track/per_genre', views.tracks_count_per_genre, name='track_count_per_genre'),
]