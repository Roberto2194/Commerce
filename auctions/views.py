from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings.filter(isActive=True)
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    if request.method == "POST":
        try:
            category = request.POST["category"]
            listings = AuctionListing.objects.filter(category=category, isActive=True)
            return render(request, "auctions/categories.html", {
                "listings": listings
            })
        except:
            return render(request, "auctions/categories.html", {
                "message": "Pick a category."
            })
    else:
        return render(request, "auctions/categories.html")


def watchlist(request):
    user = User.objects.get(username=request.user)
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]

        try:
            listing = AuctionListing.objects.create(
                title=title,
                description=description,
                price=float(price),
                image=image,
                category=category,
                user=request.user,
                isActive=True
                )
            listing.save()
        except ValueError:
            return render(request, "auctions/create.html", {
                "message": "There was an error adding your listing."
            })

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")


# Clicking on a listing should take users to a
# page specific to that listing. On that page,
# users should be able to view all details about
# the listing, including the current price for
# the listing.
def listings(request, listing):
    if request.method == "POST":

        if 'add_watchlist' in request.POST:
            user = User.objects.get(username=request.user)
            user.watchlist.add(listing)

        if 'remove_watchlist' in request.POST:
            user = User.objects.get(username=request.user)
            user.watchlist.remove(listing)

        # 2- The bid must be at least as large as the starting bid,
        # and must be greater than any other bids that have been
        # placed (if any). If the bid doesn’t meet those criteria,
        # the user should be presented with an error.
        if 'place_bid' in request.POST:
            place_bid = float(request.POST["place_bid"])
            starting_price = AuctionListing.objects.get(id=listing).price
            if place_bid >= starting_price:
                # Try to get the existing value of the build,
                # if it doesn't exist it goes in except and
                # instead we create a new one
                auction_listing = AuctionListing.objects.get(id=listing)
                try:
                    bid_value = Bid.objects.get(listing=auction_listing).value
                    if place_bid > bid_value:
                        Bid.objects.filter(listing=listing).update(value=place_bid, user=request.user)
                    else:
                        return render(request, "auctions/listings.html", {
                            "listing": auction_listing,
                            "bid_value": bid_value,
                            "auction_listing_active": auction_listing.isActive,
                            "message": "The bid must be greater than any other bids that have been placed."
                        })
                except:
                    Bid.objects.create(value=place_bid, user=request.user, listing=auction_listing)
            else:
                auction_listing = AuctionListing.objects.get(id=listing, isActive=True)
                try:
                    bid_value = Bid.objects.get(listing=auction_listing).value
                except:
                    bid_value = None

                return render(request, "auctions/listings.html", {
                    "listing": auction_listing,
                    "bid_value": bid_value,
                    "auction_listing_active": auction_listing.isActive,
                    "message": "The bid must be at least as large as the starting bid."
                })

        # 3- Closing the auction makes the highest
        # bidder the winner of the auction and makes the
        # listing no longer active.
        if 'close_auction' in request.POST:
            auction_listing = AuctionListing.objects.get(id=listing)
            AuctionListing.objects.filter(id=listing).update(isActive=False)

        # 5- Users who are signed in should be able
        # to add comments to the listing page.
        if 'add_comment' in request.POST:
            comment = request.POST["add_comment"]
            auction_listing = AuctionListing.objects.get(id=listing)
            Comment.objects.create(value=comment, user=request.user, listing=auction_listing)

        return HttpResponseRedirect(listing)

    elif request.method == "GET":
        try:
            auction_listing = AuctionListing.objects.get(id=listing)
            auction_listing_active = auction_listing.isActive
            # 4- If a user is signed in on a closed listing page, and
            # the user has won that auction, the page should say so.
            highest_bidder = None
            if not auction_listing_active:
                bidder = Bid.objects.get(listing=auction_listing).user
                if bidder == request.user:
                    highest_bidder = request.user
        except:
            return HttpResponse("<h1>The listing you are looking for is no longer present.</h1>")

        # 5- The listing page should display all
        # comments that have been made on the listing.
        try:
            comments = Comment.objects.filter(listing=auction_listing)
        except:
            print("Couldn't retrieve comments.")

        # 2- Display the starting price or the bid value accordingly
        bid_value = None
        current_bidder = False
        try:
            bid_value = Bid.objects.get(listing=auction_listing).value
            bidder = Bid.objects.get(listing=auction_listing).user
            if bidder == request.user:
                current_bidder = True
        except:
            print("Couldn't retrieve the bid value.")

        if request.user.is_authenticated:
            # 1- If the user is signed in, the user should be able to add
            # the item to their “Watchlist.” If the item is already on
            # the watchlist, the user should be able to remove it.
            user = User.objects.get(username=request.user)
            watchlist = user.watchlist.all()
            in_watchlist = False
            for item in watchlist:
                if str(item) == auction_listing.title:
                    in_watchlist = True

            # 3- If the user is signed in and is the one who created
            # the listing, the user should have the ability to “close”
            # the auction from this page
            can_close = (request.user == auction_listing.user)

        else:
            in_watchlist = False
            can_close = False
            highest_bidder = None

        return render(request, "auctions/listings.html", {
            "listing": auction_listing,
            "auction_listing_active": auction_listing_active,
            "highest_bidder": highest_bidder,
            "in_watchlist": in_watchlist,
            "bid_value": bid_value,
            "current_bidder": current_bidder,
            "can_close": can_close,
            "comments": comments
        })