from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from .models import Listing, User, Bid, Comment


def index(request):
    listings = Listing.objects.select_related("owner").all()
    categories = Listing.CATEGORY_CHOICES
    context = {
        "listings": listings,
        "categories": categories,
        "selected_category": None
    }
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": Listing.CATEGORY_CHOICES,
        "selected_category": None
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "auctions/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
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


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    owner = listing.owner
    highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()
    highest_bidder = highest_bid.bidder if highest_bid else None
    comments = Comment.objects.filter(listing=listing).order_by("timestamp")

    # Close listing (owner only)
    if request.method == "POST" and "close_listing" in request.POST:
        if request.user == listing.owner:
            listing.is_closed = True
            listing.save()
        return redirect("listing", listing_id=listing.id)

    # Watchlist toggle
    if request.method == "POST" and "toggle_watchlist" in request.POST:
        if request.user.is_authenticated:
            if request.user in listing.watchers.all():
                listing.watchers.remove(request.user)
            else:
                listing.watchers.add(request.user)
        return redirect("listing", listing_id=listing.id)

    # Bid submission
    if request.method == "POST" and request.POST.get("action") == "bid":
        # auth check
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to place a bid.")
            return redirect("listing", listing_id=listing_id)

        bid_amount = request.POST.get("bid")
        if not bid_amount or not bid_amount.isdigit():
            messages.error(request, "Invalid bid amount.")
            return redirect("listing", listing_id=listing_id)

        bid_amount = int(bid_amount)
        min_valid_bid = highest_bid.amount + 1 if highest_bid else listing.price
        if bid_amount < min_valid_bid:
            messages.error(request, f"Your bid must be at least ${min_valid_bid}.")
            return redirect("listing", listing_id=listing_id)

        Bid.objects.create(listing=listing, bidder=request.user, amount=bid_amount)
        listing.highest_bid = bid_amount
        listing.save()

        messages.success(request, "Your bid has been placed successfully!")
        return redirect("listing", listing_id=listing_id)

    # Comment submission
    if request.method == "POST" and request.POST.get("action") == "comment":
        if request.user.is_authenticated:
            content = request.POST.get("comment")
            if content:
                Comment.objects.create(
                    listing=listing,
                    user=request.user,
                    content=content,
                    timestamp=timezone.now()
                )
        return redirect("listing", listing_id=listing.id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "owner": owner,
        "highest_bid": highest_bid.amount if highest_bid else None,
        "highest_bidder": highest_bidder,
        "comments": comments
    })

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def make_listing(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name", "").strip()
        description = request.POST.get("description", "").strip()
        image_link = request.POST.get("image_link", "")
        price = request.POST.get("price")

        # Validate price
        if not price or not price.isdigit() or int(price) < 0:
            return render(request, "auctions/make_listing.html", {
                "message": "Price must be a non-negative number."
            })

        try:
            Listing.objects.create(
                item_name=item_name,
                description=description,
                price=int(price),
                owner=request.user,
                image_link=image_link
            )
        except IntegrityError:
            return render(request, "auctions/make_listing.html", {
                "message": "There was a problem saving your listing."
            })

        return redirect("index")

    return render(request, "auctions/make_listing.html")

def category(request, category_code):
    listings = Listing.objects.filter(category=category_code, is_closed=False)
    categories = Listing.CATEGORY_CHOICES

    return render(request, "auctions/index.html", {
        "listings": listings,
        "selected_category": category_code,
        "categories": categories,
    })