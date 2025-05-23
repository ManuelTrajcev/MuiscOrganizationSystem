# Generated by Django 5.1.3 on 2025-05-07 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0005_alter_deletedcustomerlog_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="deletedcustomerlog",
            options={"managed": False},
        ),
        migrations.AlterModelOptions(
            name="invoice",
            options={"managed": False},
        ),
        migrations.AlterModelOptions(
            name="invoiceline",
            options={"managed": False},
        ),
        migrations.AlterModelOptions(
            name="playlisttrack",
            options={"managed": False},
        ),
        migrations.CreateModel(
            name="Price",
            fields=[
                ("price_id", models.AutoField(primary_key=True, serialize=False)),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateTimeField()),
                (
                    "track_id",
                    models.ForeignKey(
                        db_column="track_id",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="music.track",
                    ),
                ),
            ],
            options={
                "db_table": "price",
            },
        ),
    ]
