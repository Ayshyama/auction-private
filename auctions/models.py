from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?[0-9]{1,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    watchlist = models.ManyToManyField(
        'AuctionListing', blank=True, related_name="userWatchlist")





class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.id} : {self.name}"


class AuctionListing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    end_date = models.DateTimeField()
    startBid = models.DecimalField(decimal_places=0, max_digits=10)
    description = models.TextField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imageUrl = models.URLField(null = True, blank=True)
    auc_image = models.ImageField(blank=True, upload_to='auc_images/')
    active = models.BooleanField()



    def __str__(self):
        return f"{self.id} : {self.name} in {self.category.name}\nPosted at : {self.date}\nValue : {self.startBid}\nDescription : {self.description}\nPosted By : {self.user.username} Active Status: {self.active}"


class Bid(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidValue = models.DecimalField(decimal_places=0, max_digits=10)
    auctionListing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} : {self.user.username} bid {self.bidValue} on {self.auctionListing.name} at {self.date}"


class Comment(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auctionListing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)
    commentValue = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id} : {self.user.username} commented on {self.auctionListing.name} posted by {self.auctionListing.user.username} at {self.date} : {self.commentValue}"
    
