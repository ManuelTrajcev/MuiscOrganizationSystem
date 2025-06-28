import json

from django.shortcuts import render
import os
import django
from django.db import connection
from django.shortcuts import redirect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MuiscOrganizationSystem.settings')
django.setup()

from music.models import *


# Create your views here.

def home_page(request):
    return render(request, 'home.html')


def redirect_to_home(request, exception):
    return redirect('home_page')


## LIST OF ALL ##
def album_list(request):
    search_track = request.GET.get('search_track', '').strip()

    if search_track:
        data = Album.objects.filter(title__icontains=search_track).values_list('title', flat=True)
    else:
        data = Album.objects.all().values_list('title', flat=True)

    heading = request.GET.get('model', 'All Albums')
    return render(request, 'list.html', {
        'data': data,
        'heading': heading,
        'search_track': search_track,
    })


def track_list(request):
    search_track = request.GET.get('search_track', '').strip()

    if search_track:
        data = Track.objects.filter(name__icontains=search_track).values_list('name', flat=True)
    else:
        data = Track.objects.all().values_list('name', flat=True)

    heading = request.GET.get('model', 'All Tracks')
    return render(request, 'list.html', {'data': data, 'heading': heading, 'search_track': search_track, })


def artist_list(request):
    search_track = request.GET.get('search_track', '').strip()

    if search_track:
        data = Artist.objects.filter(name__icontains=search_track).values_list('name', flat=True)
    else:
        data = Artist.objects.all().values_list('name', flat=True)
    heading = request.GET.get('model', 'All Artists')

    return render(request, 'list.html', {'data': data, 'heading': heading, 'search_track': search_track, })


## VIEWS ##
def tracks_count_per_genre(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM track_count_per_genre;")
        rows = cursor.fetchall()

    data = [{'genre': row[0], 'count': row[1]} for row in rows]

    return render(request, 'track_count_per_genre.html', {'data': data})


def avg_track_duration(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM avg_track_duration_per_artist;")
        rows = cursor.fetchall()

    data = [{'artist': row[0], 'avg': row[1]} for row in rows]

    return render(request, 'avg_track_duration.html', {'data': data})


def rank_list_most_active_customers(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rank_list_most_active_customers_view;")
        rows = cursor.fetchall()

    data = [{'name': row[0], 'total_orders': row[1], 'total_money_spent': row[2]} for row in rows]

    return render(request, 'rank_list_most_active_customers.html', {'data': data})


def avg_price_per_artist(request):
    search_track = request.GET.get('search_track', '').strip()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM avg_price_per_artist;")
        rows = cursor.fetchall()

    if search_track:
        rows = [row for row in rows if search_track.lower() in row[0].lower()]

    data = [{'name': row[0], 'avg_price_per_track': row[1]} for row in rows]

    return render(request, 'avg_price_per_artist.html', {'data': data, 'search_track': search_track})


def rank_list_artists(request):
    search_track = request.GET.get('search_track', '').strip()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rank_list_artists;")
        rows = cursor.fetchall()

    if search_track:
        rows = [row for row in rows if search_track.lower() in row[0].lower()]

    data = [{'name': row[0], 'num_invoices': row[1], 'money_earned': row[2]} for row in rows]

    return render(request, 'rank_list_artists.html', {'data': data, 'search_track': search_track})


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


## QUERRIES ##

def genres_per_customer(request):
    customers = Customer.objects.all()
    selected_customer_id = request.GET.get('customer_id')
    data = []
    customer = None

    if selected_customer_id:
        customer = Customer.objects.filter(customer_id=selected_customer_id).first()
        query = """
            SELECT c.first_name as first_name, c.last_name as last_name, g.name as genre, COUNT(tr.track_id) as track_count
            FROM customer c
            LEFT JOIN invoice i ON c.customer_id = i.customer_id
            LEFT JOIN invoice_line il ON i.invoice_id = il.invoice_id
            LEFT JOIN track tr ON il.track_id = tr.track_id
            LEFT JOIN genre g ON tr.genre_id = g.genre_id
            WHERE c.customer_id = %s
            GROUP BY c.customer_id, c.first_name, c.last_name, g.genre_id, g.name
            ORDER BY c.first_name
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [selected_customer_id])
            rows = cursor.fetchall()
            data = [{'first_name': row[0], 'last_name': row[1], 'genre': row[2], 'track_count': row[3]} for row in rows]

    return render(request, 'genres_per_customer.html', {
        'customers': customers,
        'data': data,
        'customer': customer,
        'selected_customer_id': selected_customer_id,
    })


def most_popular_artist_per_customer_per_genre(request):
    customers = Customer.objects.all()
    selected_customer_id = request.GET.get('customer_id')
    data = []
    customer = []
    if selected_customer_id:
        query = """WITH PlayCounts AS (
                SELECT
                    g.genre_id,
                    g.name AS genre_name,
                    ar.name AS artist_name,
                    COUNT(*) AS play_count
                FROM customer c
                JOIN invoice i ON c.customer_id = i.customer_id
                JOIN invoice_line il ON i.invoice_id = il.invoice_id
                JOIN track tr ON il.track_id = tr.track_id
                JOIN genre g ON tr.genre_id = g.genre_id
                JOIN album a ON tr.album_id = a.album_id
                JOIN artist ar ON a.artist_id = ar.artist_id
                WHERE c.customer_id = %s
                GROUP BY g.genre_id, g.name, ar.name
            ),
            MaxPlayCounts AS (
                SELECT genre_id, MAX(play_count) AS max_count
                FROM PlayCounts
                GROUP BY genre_id
            )
            SELECT pc.genre_name, pc.artist_name, pc.play_count
            FROM PlayCounts pc
            JOIN MaxPlayCounts mpc ON pc.genre_id = mpc.genre_id AND pc.play_count = mpc.max_count;
        """
        customer = Customer.objects.filter(customer_id=selected_customer_id).first()

        with connection.cursor() as cursor:
            cursor.execute(query, [selected_customer_id])
            rows = cursor.fetchall()
            data = [{'genre': row[0], 'arist': row[1]} for row in rows]

    return render(request, 'most_popular_artist_per_customer_per_genre.html', {
        'customers': customers,
        'customer': customer,
        'data': data,
        'selected_customer_id': selected_customer_id,
    })


def invoice_per_customer_after_date(request):
    customers = Customer.objects.all()
    selected_customer_id = request.GET.get('customer_id')
    selected_date = request.GET.get('invoice_date', '2000-01-01')
    data = []
    sum = 0
    customer = None

    if selected_customer_id:
        customer = Customer.objects.filter(customer_id=selected_customer_id).first()
        if selected_date:
            query = """
                SELECT c.first_name, c.last_name, i.invoice_date::date, i.total
                FROM customer c
                JOIN invoice i ON c.customer_id = i.customer_id
                WHERE c.customer_id = %s AND i.invoice_date > %s
                ORDER BY i.invoice_date
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [selected_customer_id, selected_date])
                rows = cursor.fetchall()
                for r in rows:
                    sum += r[3]

                data = [{'first_name': row[0], 'last_name': row[1], 'invoice_date': row[2], 'total': row[3]} for row in
                        rows]
        else:
            query = """
                            SELECT c.first_name, c.last_name, i.invoice_date::date, i.total
                            FROM customer c
                            JOIN invoice i ON c.customer_id = i.customer_id
                            WHERE c.customer_id = %s
                            ORDER BY i.invoice_date
                        """
            with connection.cursor() as cursor:
                cursor.execute(query, [selected_customer_id])
                rows = cursor.fetchall()
                for r in rows:
                    sum += r[3]

                data = [{'first_name': row[0], 'last_name': row[1], 'invoice_date': row[2], 'total': row[3]}
                        for row in
                        rows]

    return render(request, 'invoices_per_customer_after_date.html', {
        'customers': customers,
        'total_sum': sum,
        'data': data,
        'customer': customer,
        'selected_customer_id': selected_customer_id,
    })


from django.shortcuts import render, redirect
from music.models import Employee
from django.contrib import messages


def batch_update_reports_to(request):
    selected_manager_id = request.POST.get('manager_id') or request.GET.get('manager_id')
    employees = Employee.objects.exclude(
        employee_id=selected_manager_id) if selected_manager_id else Employee.objects.all()

    if request.method == 'POST':
        selected_employee_ids = request.POST.getlist('employee_ids')

        if selected_manager_id and selected_employee_ids:
            json_data = json.dumps([
                {"employee_id": int(emp_id), "reports_to_id": int(selected_manager_id)}
                for emp_id in selected_employee_ids
            ])
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT batch_update_reports_to(%s::json);", [json_data])
                messages.success(request, "Batch update successful.")
                return redirect('batch_update_reports_to')

            except Exception as e:
                messages.error(request, f"Error during update: {e}")

    all_employees = Employee.objects.all()
    return render(request, 'batch_update_reports_to.html', {
        'employees': employees,
        'all_employees': all_employees,
        'selected_manager_id': selected_manager_id
    })


def add_tracks_to_playlist(request):
    search_track = request.GET.get('search_track', '').strip()

    invoices = Invoice.objects.all()

    if search_track:
        tracks = Track.objects.filter(name__icontains=search_track)
    else:
        tracks = Track.objects.all()

    playlists = Playlist.objects.all()
    selected_playlist_id = request.POST.get('playlist_id') or request.GET.get('playlist_id')

    if request.method == 'POST':
        selected_track_ids = request.POST.getlist('track_ids')

        if selected_playlist_id and selected_track_ids:
            json_data = json.dumps([
                {"track_id": int(track_id)}
                for track_id in selected_track_ids
            ])
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT add_tracks_to_playlist(%s, %s::json);", [selected_playlist_id, json_data])
                messages.success(request, "Tracks successfully added to playlist.")
                return redirect('add_tracks_to_playlist')

            except Exception as e:
                messages.error(request, f"Error adding tracks: {e}")

    return render(request, 'add_tracks_to_playlist.html', {
        'playlists': playlists,
        'tracks': tracks,
        'selected_playlist_id': selected_playlist_id,
        'search_track': search_track,
    })


def add_invoice_lines_to_invoice(request):
    search_track = request.GET.get('search_track', '').strip()

    invoices = Invoice.objects.all().order_by('invoice_id')

    if search_track:
        tracks = Track.objects.filter(name__icontains=search_track)
    else:
        tracks = Track.objects.all()

    selected_invoice_id = request.POST.get('invoice_id') or request.GET.get('invoice_id')

    if request.method == 'POST':
        selected_track_ids = request.POST.getlist('track_ids')
        quantities = request.POST.getlist('quantities')

        if selected_invoice_id and selected_track_ids and quantities:
            try:
                invoice_lines = []
                for i in range(len(selected_track_ids)):
                    track_id = int(selected_track_ids[i])
                    quantity = int(quantities[i])
                    invoice_lines.append({'track_id': track_id, 'quantity': quantity})

                json_data = json.dumps(invoice_lines)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT add_invoice_lines_to_existing_invoice(%s, %s::json);",
                                   [selected_invoice_id, json_data])

                messages.success(request, "Invoice lines added successfully.")
                return redirect('add_invoice_lines_to_invoice')

            except Exception as e:
                messages.error(request, f"Error adding invoice lines: {e}")

    return render(request, 'add_invoice_lines_to_invoice.html', {
        'invoices': invoices,
        'tracks': tracks,
        'selected_invoice_id': selected_invoice_id,
        'search_track': search_track,
    })
