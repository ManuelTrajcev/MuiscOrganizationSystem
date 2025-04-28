from django.shortcuts import render
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MuiscOrganizationSystem.settings')
django.setup()

from music.models import *


# Create your views here.

def album_list(request):
    heading = request.GET.get('model', 'All Albums')
    data = Album.objects.values_list('title', flat=True)
    return render(request, 'list.html', {'data': data, 'heading': heading})


def track_list(request):
    heading = request.GET.get('model', 'All Tracks')
    data = Track.objects.values_list('name', flat=True)
    return render(request, 'list.html', {'data': data, 'heading': heading})


def artist_list(request):
    heading = request.GET.get('model', 'All Artists')
    data = Artist.objects.values_list('name', flat=True)
    print(data)
    return render(request, 'list.html', {'data': data, 'heading': heading})


# VIEWS
def tracks_count_per_genre(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM track_count_per_genre;")
        rows = cursor.fetchall()

    data = [{'genre': row[0], 'count': row[1]} for row in rows]
    print(data)

    return render(request, 'track_count_per_genre.html', {'data': data})


def avg_track_duration(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM avg_track_duration_per_artist;")
        rows = cursor.fetchall()

    data = [{'artist': row[0], 'avg': row[1]} for row in rows]
    print(data)

    return render(request, 'avg_track_duration.html', {'data': data})


def rank_list_most_active_customers(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rank_list_most_active_customers_view;")
        rows = cursor.fetchall()

    data = [{'name': row[0], 'total_orders': row[1], 'total_money_spent': row[2]} for row in rows]

    return render(request, 'rank_list_most_active_customers.html', {'data': data})


def avg_price_per_artist(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM avg_price_per_artist;")
        rows = cursor.fetchall()

    data = [{'name': row[0], 'avg_price_per_track': row[1]} for row in rows]

    return render(request, 'avg_price_per_artist.html', {'data': data})


def rank_list_artists(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rank_list_artists;")
        rows = cursor.fetchall()

    data = [{'name': row[0], 'num_invoices': row[1]} for row in rows]

    return render(request, 'rank_list_artists.html', {'data': data})



def media_type_percentage(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM media_type_percentage;")
        rows = cursor.fetchall()

    data = [{'name': row[0], 'num_of_tracks': row[1], 'percentage': row[2]} for row in rows]

    return render(request, 'media_type_percentage.html', {'data': data})


def most_listened_genre_per_customer(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM most_listened_genre_per_customer;")
        rows = cursor.fetchall()

    data = [{'first_name': row[0], 'last_name': row[1], 'most_listened_genre': row[2]} for row in rows]

    return render(request, 'most_listened_genre_per_customer.html', {'data': data})
