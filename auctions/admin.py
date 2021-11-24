from django.contrib import admin
from .models import User, Category, Product, Bid, Lot, Comment
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Lot)
admin.site.register(Comment)