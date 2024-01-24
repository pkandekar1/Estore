
from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('home2',views.home2),
    path('home3',views.home3),
    path('range',views.range),
    path('sort/<sv>',views.sort),
    path('addtocart/<pid>',views.addtocart),
    path('catfilter/<cv>',views.catfilter),
    path('registration',views.registration),
    path('d',views.dummyregistration),
    path('login',views.login_user),
    path('logout',views.user_logout),
    path('pd/<pid>',views.product_detail),
    path('po',views.place_order),
    path('cart',views.cart),
    path('remove/<cid>',views.remove),
    path('Remove/<cid>',views.Remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('about',views.about),
    path('contact',views.contact),
    path('add/<a>/<b>',views.addition),
    path('makepayment',views.makepayment),
    path('sendusermail',views.sendusermail),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
