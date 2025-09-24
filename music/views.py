import json

from django.shortcuts import render
import os
import django
from django.db import connection
from django.shortcuts import redirect
from django.utils import timezone

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
        data = Album.objects.filter(
            title__icontains=search_track,
            deleted_at__isnull=True
        ).values_list('title', flat=True)
    else:
        data = Album.objects.filter(
            deleted_at__isnull=True
        ).values_list('title', flat=True)

    heading = request.GET.get('model', 'All Albums')
    return render(request, 'list.html', {
        'data': data,
        'heading': heading,
        'search_track': search_track,
    })


def track_list(request):
    search_track = request.GET.get('search_track', '').strip()

    if search_track:
        data = Track.objects.filter(
            name__icontains=search_track,
            deleted_at__isnull=True
        ).values_list('name', flat=True)
    else:
        data = Track.objects.filter(
            deleted_at__isnull=True
        ).values_list('name', flat=True)

    heading = request.GET.get('model', 'All Tracks')
    return render(request, 'list.html', {'data': data, 'heading': heading, 'search_track': search_track, })


def artist_list(request):
    search_track = request.GET.get('search_track', '').strip()

    if search_track:
        data = Artist.objects.filter(
            name__icontains=search_track,
            deleted_at__isnull=True
        ).values_list('name', flat=True)
    else:
        data = Artist.objects.filter(
            deleted_at__isnull=True
        ).values_list('name', flat=True)

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
            WITH CustomerTracks AS (
                SELECT
                    c.customer_id,
                    c.first_name,
                    c.last_name,
                    g.genre_id,
                    g.name AS genre_name,
                    tr.track_id
                FROM customer c
                LEFT JOIN invoice i ON c.customer_id = i.customer_id
                LEFT JOIN invoice_line il ON i.invoice_id = il.invoice_id
                LEFT JOIN track tr ON il.track_id = tr.track_id
                LEFT JOIN genre g ON tr.genre_id = g.genre_id
                WHERE c.customer_id = %s
            ),
            GenreCounts AS (
                SELECT
                    customer_id,
                    first_name,
                    last_name,
                    genre_id,
                    genre_name,
                    COUNT(track_id) AS track_count
                FROM CustomerTracks
                GROUP BY customer_id, first_name, last_name, genre_id, genre_name
            )
            SELECT
                first_name,
                last_name,
                genre_name,
                track_count
            FROM GenreCounts
            ORDER BY first_name, genre_name;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [selected_customer_id])
            rows = cursor.fetchall()
            data = [
                {
                    'first_name': row[0],
                    'last_name': row[1],
                    'genre': row[2],
                    'track_count': row[3]
                }
                for row in rows
            ]

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
    selected_date = request.GET.get('invoice_date')

    # normalize empty or None date
    if not selected_date:
        selected_date = '2000-01-01'

    data = []
    total_sum = 0
    customer = None

    if selected_customer_id:
        customer = Customer.objects.filter(customer_id=selected_customer_id).first()

        query = """
            WITH CustomerInvoices AS (
                SELECT 
                    c.customer_id,
                    c.first_name,
                    c.last_name,
                    i.invoice_date::date AS invoice_date,
                    i.total
                FROM customer c
                JOIN invoice i ON c.customer_id = i.customer_id
                WHERE c.customer_id = %s
                  AND i.invoice_date > %s
            ),
            InvoiceTotals AS (
                SELECT customer_id, SUM(total) AS total_sum
                FROM CustomerInvoices
                GROUP BY customer_id
            )
            SELECT
                ci.first_name,
                ci.last_name,
                ci.invoice_date,
                ci.total,
                it.total_sum
            FROM CustomerInvoices ci
            JOIN InvoiceTotals it ON ci.customer_id = it.customer_id
            ORDER BY ci.invoice_date;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [selected_customer_id, selected_date])
            rows = cursor.fetchall()
            if rows:
                total_sum = rows[0][4]
            data = [
                {
                    'first_name': row[0],
                    'last_name': row[1],
                    'invoice_date': row[2],
                    'total': row[3]
                }
                for row in rows
            ]

    return render(request, 'invoices_per_customer_after_date.html', {
        'customers': customers,
        'total_sum': total_sum,
        'data': data,
        'customer': customer,
        'selected_customer_id': selected_customer_id,
        'selected_date': selected_date,  # keep it in context if needed
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


def create_invoice(request):
    customers = Customer.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        billing_address = request.POST.get("billing_address")
        billing_city = request.POST.get("billing_city")
        billing_country = request.POST.get("billing_country")
        billing_postal_code = request.POST.get("billing_postal_code")
        billing_state = request.POST.get("billing_state")

        # You may want to add validation here
        if customer_id and billing_address and billing_city and billing_country:
            invoice = Invoice.objects.create(
                customer_id=customer_id,
                invoice_date=timezone.now(),
                billing_address=billing_address,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_country=billing_country,
                billing_postal_code=billing_postal_code,
                total=0
            )
            return redirect("create_invoice")
            # or redirect to invoice list page

    return render(request, "create_invoice.html", {"customers": customers})


def create_customer(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        company = request.POST.get("company")
        support_rep_id = request.POST.get("support_rep_id")

        phone = request.POST.get("phone")
        fax = request.POST.get("fax")
        email = request.POST.get("email")

        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        postalcode = request.POST.get("postalcode")

        contact = Contact.objects.create(phone=phone, fax=fax, email=email)
        address_info = AddressInfo.objects.create(
            address=address, city=city, state=state, country=country, postal_code=postalcode
        )

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            company=company,
            support_rep_id=support_rep_id if support_rep_id else None,
            contact=contact,
            address_info=address_info
        )

        return redirect("create_customer")

    return render(request, "create_customer.html", {"employees": employees})


def create_playlist(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Playlist.objects.create(name=name)
            return redirect("create_playlist")
    return render(request, "create_playlist.html")


def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
              AND table_type='BASE TABLE';
        """)
        return [row[0] for row in cursor.fetchall()]


def delete_records(request):
    tables = list_tables()
    selected_table = request.GET.get("table") or request.POST.get("table")
    search_query = request.GET.get("search", "").strip()
    rows, cols = [], []

    if selected_table:
        with connection.cursor() as cursor:
            # Get column names
            cursor.execute(f"SELECT * FROM {selected_table} WHERE deleted_at IS NULL;")
            cols = [desc[0] for desc in cursor.description]

            if search_query:
                conditions = " OR ".join([f"CAST({col} AS TEXT) ILIKE %s" for col in cols])
                params = [f"%{search_query}%"] * len(cols)
                cursor.execute(f"SELECT * FROM {selected_table} WHERE {conditions} AND deleted_at IS NULL;", params)
            else:
                cursor.execute(f"SELECT * FROM {selected_table} WHERE deleted_at IS NULL;")

            rows = [dict(zip(cols, r)) for r in cursor.fetchall()]

        for row in rows:
            row["pk"] = row[cols[0]]

    if request.method == "POST" and selected_table:
        ids = request.POST.getlist("record_ids")
        if ids:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {selected_table} WHERE {cols[0]} IN %s;",
                    (tuple(ids),)
                )
        return redirect("delete_records")

    return render(request, "delete_records.html", {
        "tables": tables,
        "selected_table": selected_table,
        "rows": rows,
        "cols": cols if selected_table else [],
        "search_query": search_query,
    })
