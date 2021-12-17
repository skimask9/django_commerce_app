from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Lot', blank=True, related_name="userWatchlist")

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    def __str__(self):
        return f"{self.id} . {self.name}"

class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    image = models.URLField(blank=True)
    description = models.CharField(max_length=500)
    detailed = models.URLField(max_length = 200,unique=True,null=True) 
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.ForeignKey(Category, max_length=60, on_delete=models.CASCADE, related_name= 'categories')
    def __str__(self):
        return f"{self.id} : {self.title}"



class Lot(models.Model):
    lot_name = models.CharField(max_length=64)
    lot_price = models.DecimalField(decimal_places=2, max_digits=7) 
    lot_description = models.CharField(max_length=70)
    lot_date = models.DateTimeField(auto_now_add=True)
    lot_status = models.BooleanField()
    lot_author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    lot_category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="category_lot")
    lot_image = models.URLField(blank=True)
    def __str__(self):
        return f"{self.id}: {self.lot_name} in {self.lot_category} Posted at : {self.lot_date} Value :{self.lot_price} \nDescription :{self.lot_description} Posted By : {self.lot_author} Active Status: {self.lot_status}  "

class Bid(models.Model):
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bid_value = models.DecimalField(decimal_places=2, max_digits=7)
    lotbid = models.ForeignKey(Lot, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.bid_user.username} bid {self.bid_value} on {self.lotbid.lot_name} at {self.bid_date}"



class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    commentValue = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id} : {self.user.username} commented on {self.lot.lot_name} posted by {self.lot.lot_author.username} at {self.date} : {self.commentValue}"        