# Generated by Django 4.2.2 on 2023-06-16 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_alter_auctionlisting_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="isActive",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="auctionlisting",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
