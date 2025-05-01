from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('album/', views.album_list, name='album_list'),
    path('artist/', views.artist_list, name='artist_list'),
    path('artist/avg-track-duration', views.avg_track_duration, name='avg_track_duration'),
    path('artist/avg-track-price', views.avg_price_per_artist, name='avg_track_price'),
    path('artist/most-popular', views.rank_list_artists, name='rank_list_artists'),
    path('track/', views.track_list, name='track_list'),
    path('customer/genres-per-customer', views.genres_per_customer, name='genres_per_customer'),
    path('customer/invoices-per-customer', views.invoice_per_customer_after_date,
         name='invoice_per_customer_after_date'),
    path('customer/artist-per-genre', views.most_popular_artist_per_customer_per_genre,
         name='most_popular_artist_per_customer_per_genre'),
    path('customer/most-popular-genre-per-customer', views.most_listened_genre_per_customer,
         name='most_listened_genre_per_customer'),
    path('media-type/percentage', views.media_type_percentage, name='media_type_percentage'),
    path('track/per-genre', views.tracks_count_per_genre, name='track_count_per_genre'),
    path('customer/rank-list', views.rank_list_most_active_customers, name='rank_list_most_active_customers'),
]
