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
    return render(request, 'album_list.html', {'data': data, 'heading': heading})


def track_list(request):
    heading = request.GET.get('model', 'All Tracks')
    data = Track.objects.values_list('name', flat=True)
    return render(request, 'album_list.html', {'data': data, 'heading': heading})


def tracks_count_per_genre(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM track_count_per_genre;")
        rows = cursor.fetchall()

    data = [{'genre': row[0], 'count': row[1]} for row in rows]
    print(data)

    return render(request, 'track_count_per_genre.html', {'data': data})


def artist_list(request):
    heading = request.GET.get('model', 'All Artists')
    data = Artist.objects.values_list('name', flat=True)
    print(data)
    return render(request, 'album_list.html', {'data': data, 'heading': heading})
