from django.contrib.auth.models import AbstractUser
from django.db import models


# Your application should have at least
# three models in addition to the User model:
class User(AbstractUser):
    watchlist = models.ManyToManyField("AuctionListing", blank=True, related_name="watchlist")
    pass


# one for auction listings
class AuctionListing(models.Model):
    BROOMSTICK = 'Broomstick'
    ROBE = 'Robe'
    BOOK = 'Book'
    WAND = 'Wand'
    QUILL = 'Quill'

    CATEGORY_TYPE = [(BROOMSTICK, 'Broomstick'), (ROBE, 'Robe'), (BOOK, 'Book'), (WAND, 'Wand'), (QUILL, 'Quill')]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=256)
    category = models.CharField(max_length=32, choices=CATEGORY_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="owner")
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# one for bids
class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bidder")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, related_name="item")

    def __str__(self):
        return f"Highest bid on {self.listing}: ${self.value} made by {self.user}"


# and one for comments made on auction listings
class Comment(models.Model):
    value = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="author")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, related_name="listing")

    def __str__(self):
        return f"Comment on {self.listing}: {self.value} made by {self.user}"

