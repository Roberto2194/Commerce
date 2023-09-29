# Generated by Django 4.2.2 on 2023-06-16 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_rename_bids_bid_rename_comments_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bidder",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="bid",
            name="value",
            field=models.DecimalField(decimal_places=2, default=False, max_digits=10),
        ),
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="value",
            field=models.DecimalField(decimal_places=2, default=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="category",
            field=models.CharField(
                choices=[
                    ("BR", "Broom"),
                    ("CL", "Cloak"),
                    ("BK", "Book"),
                    ("WN", "Wand"),
                    ("QL", "Quill"),
                ],
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]