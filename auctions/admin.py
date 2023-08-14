from django.contrib import admin
from .models import Category, AuctionListing, User, Comment, Bid
from django.forms import DateTimeInput
from django.db import models

# Register your models here.
admin.site.register(User)
admin.site.register(Category)

admin.site.register(Bid)
admin.site.register(Comment)

admin.site.register(AuctionListing)