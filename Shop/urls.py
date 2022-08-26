from django.urls import path, include

from .views import *
from .apiviews import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'comment', CommentAPIView)
router.register(r'product', ProductViewSet)
router.register(r'rating', AddStarRatingViewSet)

# print (router.urls)


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('shop/', ShopView.as_view(), name = 'shop'),
    path('shop/<int:pk>', ShopView.as_view(), name = 'shop_pk'),
    path('filtershop/', FilterShopView.as_view(), name = 'filter'),
    path('filtershop/<int:pk>', FilterShopView.as_view(), name = 'filter_pk'),
    path('product/<slug:slug>', ProductView.as_view(), name = 'product'),
    path('cart/', CartView.as_view(), name = 'cart' ),
    path('checkout/', CheckoutView.as_view(), name = 'checkout'),

    
    path('api/', include(router.urls)),
    path('api/prof/', ProfileAPIView.as_view()),
]
