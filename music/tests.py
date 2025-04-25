from django.test import TestCase

# Create your tests here.
from django.shortcuts import render
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MuiscOrganizationSystem.settings')
django.setup()

from music.models import Artist
artists = Artist.objects.raw('SELECT * FROM music_artist')
for artist in artists:
    print(artist.name)