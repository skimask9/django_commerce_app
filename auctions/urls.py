from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all, name="all"),
    path("auctions/category/<int:category_id>", views.lotbycategory, name = 'lotbycategory'),
    path("auctions/lot/<int:lot_id>", views.lot, name = "lot"),
    path("auctions/createLot", views.createLot, name = "createLot"),
    path("auctions/lot/bid/<int:lot_id>", views.bid, name = "bid"),
    path("auctions/lot/end/<int:lot_id>", views.end, name="end"),
    path("auctions/lot/comment<int:lot_id>", views.comment, name = "comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchinglots",views.watchinglots, name= "watchinglots"),
    path("test/<str:name>", views.test, name = "test"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("products", views.products, name='products'),
    path("categories",views.categories_list, name='categories_list'),
    path("categories/<int:category_id>", views.category, name = "category")
    
]   

