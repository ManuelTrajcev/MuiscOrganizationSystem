from django.contrib import admin
from .models import *
# Register your models here.
class PlaylistTrackAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'track')

admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Genre)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(MediaType)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack, PlaylistTrackAdmin)
admin.site.register(Track)