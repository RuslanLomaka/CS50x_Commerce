from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    item_name = models.CharField(max_length=64)
    description = models.CharField(max_length=500, blank=False)
    price = models.IntegerField()  # This is the starting price
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # One-to-Many Relationship
    highest_bid = models.IntegerField(null=True, blank=True)  # Tracks current highest bid
    is_closed = models.BooleanField(default=False)  # Marks if auction is closed
    image_link = models.CharField(max_length=500, blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    CATEGORY_CHOICES = [
        ('ELEC', 'Electronics'),
        ('BOOK', 'Books'),
        ('FASH', 'Fashion'),
        ('HOME', 'Home & Garden'),
        ('TOY', 'Toys'),
        ('AUTO', 'Automotive'),
        ('SPORT', 'Sports & Outdoors'),
        ('OTHER', 'Other'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='OTHER'
    )
    def __str__(self):
        return f"{self.item_name} (${self.price}) - {self.owner.username}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.bidder.username} has bid ${self.amount} on {self.listing.item_name} by {self.listing.owner.username} at {self.timestamp}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username} on {self.listing.item_name}: {self.content}"