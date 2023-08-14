from django import template
from django.db.models import Max

from auctions.models import Bid

register = template.Library()

@register.filter
def max_bid(auction_listing):
    max_bid = Bid.objects.filter(auctionListing=auction_listing).aggregate(Max('bidValue'))['bidValue__max']
    return max_bid or 0