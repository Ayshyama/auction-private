from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("details/<int:id>", views.details, name="details"),
    path("categories", views.categories, name="categories"),
    path("filter/<str:name>", views.filter, name="filter"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("end/<int:itemId>", views.end, name="end"),
    path("all", views.all, name="all"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch", views.watch, name="watch")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Tuzov Auction House'
admin.site.site_title = 'Tuzov Auction House'
admin.site.index_title = 'Admin Panel'
