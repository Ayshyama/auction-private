from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Category, AuctionListing, Bid, Comment
from django.core.paginator import Paginator
from django.db.models import Max
from auctions.models import Bid
from .models import PartnerLogo, Announcement





def index(request):
    p = Paginator(AuctionListing.objects.all(), 10)
    page = request.GET.get('page')
    obj = p.get_page(page)

    partner_logos = PartnerLogo.objects.all()
    announcements = Announcement.objects.all()

    bids = Bid.objects.values('auctionListing').annotate(max_bid=Max('bidValue'))
    max_bids = {}
    for bid in bids:
        max_bids[bid['auctionListing']] = bid['max_bid']

    return render(request, "auctions/index.html", {
        "objects": obj,
        'bids': bids,
        'max_bids': max_bids,
        'partner_logos': partner_logos,
        'announcements': announcements
    })

def details(request, id):
    try:
        item = AuctionListing.objects.get(id=id)
    except AuctionListing.DoesNotExist:
        return HttpResponse('<script>alert("The requested item does not exist."); window.history.back();</script>')
    bids = Bid.objects.filter(auctionListing=item)
    comments = Comment.objects.filter(auctionListing=item)
    value = bids.aggregate(Max('bidValue'))['bidValue__max']
    bid = None
    if value is not None:
        bid = Bid.objects.filter(bidValue=value)[0]
    return render(request, "auctions/details.html", {
        'item': item,
        'bids': bids,
        'comments': comments,
        'bid': bid    
    })



def all(request):
    obj = AuctionListing.objects.all()
    p = Paginator(AuctionListing.objects.all(), 6)
    page = request.GET.get('page')
    obj = p.get_page(page)
    return render(request, "auctions/index.html", {
        "objects": obj,

    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        phone = request.POST["phone"]

        if not username or not password or not confirmation or not phone:
            return render(request, "auctions/register.html", {
                "message": "All fields are required."
            })

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



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


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def createListing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = request.POST["startBid"]
        category = Category.objects.get(id=request.POST["category"])
        user = request.user
        imageUrl = request.POST["url"]
        if imageUrl == '':
            imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
        listing = AuctionListing.objects.create(
            name=title, category=category, date=timezone.now(), startBid=startBid, description=description, user=user, imageUrl=imageUrl, active=True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createListing.html", {
        'categories': Category.objects.all()
    })


def auction_details(request, item_id):
    # retrieve auction listing based on item id
    auction = AuctionListing.objects.get(id=item_id)
    # render template with auction details
    context = {'auction': auction}
    return render(request, 'auction_details.html', context)


def categories(request):
    if request.method == 'POST':
        category = request.POST["category"]
        new_category, created = Category.objects.get_or_create(
            name=category.lower())
        if created:
            new_category.save()
        else:
            messages.warning(request, "Category already Exists!")
        return HttpResponseRedirect(reverse("categories"))
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })


def filter(request, name):
    category = Category.objects.get(name=name)
    obj = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "objects": obj
    })


@login_required
def comment(request, id):
    if request.method == 'POST':
        auctionListing = AuctionListing.objects.get(id=id)
        user = request.user
        commentValue = request.POST["content"].strip()
        if(commentValue != ""):
            comment = Comment.objects.create(date=timezone.now(
            ), user=user, auctionListing=auctionListing, commentValue=commentValue)
            comment.save()
        return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
    return HttpResponseRedirect(reverse("index"))



@login_required
def bid(request, id):
    if request.method == 'POST':
        auctionListing = AuctionListing.objects.get(id=id)
        bidValue = request.POST.get("bid")
        if not bidValue:
            messages.warning(request, 'Please enter a bid value!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        try:
            bidValue = float(bidValue)
        except ValueError:
            messages.warning(request, 'Please enter a valid bid value!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        args = Bid.objects.filter(auctionListing=auctionListing)
        value = args.aggregate(Max('bidValue'))['bidValue__max']
        if value is None:
            value = 0
        if bidValue < auctionListing.startBid or bidValue <= value:
            messages.warning(request, f'Bid higher than: {max(value, auctionListing.startBid)}!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        if bidValue > 1000000:
            messages.warning(request, 'Maximum bid value is 1000000!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        user = request.user
        bid = Bid.objects.create(
            date=timezone.now(), user=user, bidValue=bidValue, auctionListing=auctionListing)
        bid.save()
        messages.success(request, 'Bid placed successfully!')
    return HttpResponseRedirect(reverse("details", kwargs={'id': id}))


@login_required
def end(request, itemId):
    auctionListing = AuctionListing.objects.get(id=itemId)
    user = request.user
    if user.is_superuser:
        auctionListing.active = False
        auctionListing.save()
        messages.success(
            request, f'Auction for {auctionListing.name} successfully closed!')
    else:
        messages.info(
            request, 'You are not authorized to end this listing!')
    return HttpResponseRedirect(reverse("details", kwargs={'id': itemId}))


@login_required
def watchlist(request):
    if request.method == 'POST':
        user = request.user
        auctionListing = AuctionListing.objects.get(id=request.POST["item"])
        if request.POST["status"] == '1':
            user.watchlist.add(auctionListing)
        else:
            user.watchlist.remove(auctionListing)
        user.save()
        return HttpResponseRedirect(
            reverse("details", kwargs={'id': auctionListing.id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def watch(request):
    user = request.user
    obj = user.watchlist.all()
    return render(request, "auctions/index.html", {
        "objects": obj
    })