# Generated by Django 5.1.3 on 2025-05-07 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0003_tracks_count_per_genre"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeletedCustomerLog",
            fields=[
                ("log_id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=40)),
                ("last_name", models.CharField(max_length=20)),
                ("deleted_at", models.DateTimeField()),
                ("total_spent", models.DecimalField(decimal_places=2, max_digits=10)),
                ("invoice_count", models.IntegerField()),
            ],
            options={
                "db_table": "deleted_customer_log",
                "managed": False,
            },
        ),
        migrations.DeleteModel(
            name="tracks_count_per_genre",
        ),
        migrations.AlterModelOptions(
            name="invoice",
            options={"managed": False},
        ),
        migrations.AlterModelOptions(
            name="invoiceline",
            options={"managed": False},
        ),
    ]
