from django.contrib import admin

from auctions.models import Listing, User, Bid, Comment

# Register your models here.






class ListingAdmin(admin.ModelAdmin):
    list_display = ("item_name", "owner", "price")
    filter_horizontal = ('watchers',)


class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "listing", "timestamp", "amount")


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "timestamp", "content")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
