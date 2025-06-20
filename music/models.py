from django.db import models


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or "Unknown Artist"

    class Meta:
        db_table = 'artist'


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=160)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artist_id')
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'album'


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    title = models.CharField(max_length=30, blank=True, null=True)
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='reports_to')
    birth_date = models.DateTimeField(blank=True, null=True)
    hire_date = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'employee'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    company = models.CharField(max_length=80, blank=True, null=True)
    support_rep = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True,
                                    db_column='support_rep_id')
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'customer'


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or "Unknown Genre"

    class Meta:
        db_table = 'genre'


class MediaType(models.Model):
    media_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or "Unknown Media"

    class Meta:
        db_table = 'media_type'


class Track(models.Model):
    track_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True, db_column='album_id')
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE, db_column='media_type_id')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True, db_column='genre_id')
    composer = models.CharField(max_length=220, blank=True, null=True)
    milliseconds = models.IntegerField()
    bytes = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'track'


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, db_column='customer_id', null=True)
    invoice_date = models.DateTimeField()
    billing_address = models.CharField(max_length=70, blank=True, null=True)
    billing_city = models.CharField(max_length=40, blank=True, null=True)
    billing_state = models.CharField(max_length=40, blank=True, null=True)
    billing_country = models.CharField(max_length=40, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=10, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice #{self.invoice_id}"

    class Meta:
        db_table = 'invoice'
        managed = False


class InvoiceLine(models.Model):
    invoice_line_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_column='invoice_id')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, db_column='track_id')
    quantity = models.IntegerField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'invoice_line'
        managed = False


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or f"Playlist {self.playlist_id}"

    class Meta:
        db_table = 'playlist'


class PlaylistTrack(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='playlist_id')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, db_column='track_id')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'playlist_track'
        managed = False
        unique_together = (('playlist', 'track'),)

    def __str__(self):
        return f"{self.playlist} - {self.track}"


class DeletedCustomerLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    deleted_at = models.DateTimeField()
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_count = models.IntegerField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'deleted_customer_log'
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Deleted on {self.deleted_at} - Total Spent: ${self.total_spent} from {self.invoice_count} invoices"


class Price(models.Model):
    price_id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    track_id = models.ForeignKey(Track, on_delete=models.DO_NOTHING, db_column='track_id')

    class Meta:
        managed = False
        db_table = 'price'

    def __str__(self):
        return f"{self.track_id} - {self.value} - {self.date}"


class PersonalInfo(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='personalinfo')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personalinfo'
    def __str__(self):
        return f"Personal info for {self.customer.first_name} {self.customer.last_name}"