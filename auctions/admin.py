from django.contrib import admin
from .models import Category, AuctionListing, User, Comment, Bid
from .models import PartnerLogo, Announcement

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(AuctionListing)


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'width', 'height']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['text']

