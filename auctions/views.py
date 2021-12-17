from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import User,Product,Category,Lot,Bid,Comment

#-----just for fun products and their category list-----
#--------------------------------
def products(request):
    return render (request, "auctions/products.html",{
        'products': Product.objects.all(),       
    })

def categories_list(request):
    return render (request, 'auctions/categories_list.html',{
        "categories_list" : Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    product = category.categories.all()
    return render(request, "auctions/category.html",{
        'category' : category,
        'product' : product
    })
#--------------------------------


#----------Main Auction lots(ACTIVE)------------
def index(request):
    lot_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
    "lots": Lot.objects.filter(lot_status=True),
    'lot_categories' : lot_categories
        })

##all lots
def all(request):
    lot = Lot.objects.all()
    return render(request, "auctions/index.html", {
        'lots' : lot
    })


##lotbycategory
def lotbycategory(request, category_id):
    items = Lot.objects.all()
    category = Category.objects.get(pk=category_id)
    items = category.category_lot.all()
    return render(request, "auctions/lotbycategory.html", {
        'category' : category,
        "items": items
    })

##test cats
def test(request, name):    
    cat = Category.objects.get(name__iexact=name)
    lt = Lot.objects.filter(lot_category=cat)
    return render(request, "auctions/test.html",{
        "lts" : lt,
        "cats": Category.objects.all()
    })


##lot_detail
def lot(request, lot_id):
    lot = Lot.objects.get(pk=lot_id)
    bids = Bid.objects.filter(lotbid=lot)
    comments = Comment.objects.filter(lot=lot)
    value = bids.aggregate(Max('bid_value'))['bid_value__max']
    bid = None
    if value is not None:
        bid = Bid.objects.filter(bid_value=value)[0]
    return render(request, 'auctions/lot.html',{
        "lot" : lot,
        "bids" : bids,
        "comments": comments,
        "bid": bid
    })

##lot_bid
@login_required
def bid(request, lot_id):
    if request.method == 'POST':
        lots = Lot.objects.get(pk=lot_id)
        bid_value = request.POST["bid"]
        dict = Bid.objects.filter(lotbid=lots)
        value = dict.aggregate(Max('bid_value'))['bid_value__max']
        if value is None:
            value = 0
        if float(bid_value) < lots.lot_price or float(bid_value) <= value:
            messages.warning(request, f'Bid higher than: {max(value, lots.lot_price)}!')
            return HttpResponseRedirect(reverse("lot", kwargs={'lot_id': lot_id}))
        bid_user = request.user
        bid = Bid.objects.create(bid_date=timezone.now(), bid_user = bid_user, bid_value = bid_value, lotbid  = lots )
        bid.save()
    return HttpResponseRedirect(reverse('lot', kwargs={'lot_id':lot_id}))

##lot_end
@login_required
def end(request, lot_id):
    lot = Lot.objects.get(pk=lot_id)
    user = request.user
    if lot.lot_author == user:
        lot.lot_status = False
        lot.save()
        messages.success(
            request, f'Auction : {lot.lot_name} successfully closed!')
    else:
        messages.info(
            request, 'You are not authorized to end this listing!')
    return HttpResponseRedirect(reverse("lot", kwargs={'lot_id': lot_id}))







##lot_comments
@login_required
def comment (request, lot_id):
    if request.method == 'POST':
        lot = Lot.objects.get(pk=lot_id)
        user = request.user
        commentValue = request.POST['text'].strip()
        if(commentValue != ''):
            comment = Comment.objects.create(date = timezone.now(), user = user, lot=lot, commentValue=commentValue)
            comment.save()
        return HttpResponseRedirect(reverse('lot', kwargs={'lot_id': lot_id})) 


##watchlist
@login_required
def watchlist(request):
    if request.method == 'POST':
        user = request.user
        lot = Lot.objects.get(id=request.POST["wlist"])
        if request.POST["lotst"] == '1':
            user.watchlist.add(lot)
        else:
            user.watchlist.remove(lot)
        user.save()
        return HttpResponseRedirect(reverse('lot',kwargs={'lot_id':lot.id}))
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def watchinglots(request):
    user = request.user
    lots = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'lots' : lots
    })


##new lot form 
@login_required
def createLot(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        initialBid = request.POST["initialBid"]
        category = Category.objects.get(id = request.POST["category"])
        user = request.user
        image = request.POST["image"]
        if image == '':
            image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
        lot = Lot.objects.create(lot_name = title, lot_category = category, 
        lot_date = timezone.now(), lot_price = initialBid, lot_description = description, lot_author=user, lot_image = image , lot_status = True)
        lot.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/createLot.html", { 
        'categories' : Category.objects.all()
    })




#-----------unfinished---------------------------------------
#def lotcategory(request, lot_id):
    #if request.method ==  "POST":
        #lot = Lot.objects.get(pk=lot_id)
        #categoryid = int(request.POST['category'])
        #category = Category.objects.get(pk=categoryid)
        #lot=category
        #return HttpResponseRedirect(reverse('category', args=(lot.id,)))

#--------------------------------------------------
##-------------login register logout---------------
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
