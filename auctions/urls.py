from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("make_listing/", views.make_listing, name="make_listing"),
    path("category/<str:category_code>/", views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
]
