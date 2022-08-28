from django.urls import path, include

from .views import HomeView, ProfileView, ShopView, FilterShopView, ProductView, CartView
from .apiviews import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('comment', CommentAPIView)
router.register('product', ProductViewSet)
router.register('rating', AddStarRatingViewSet)
router.register('cart', CartApiView, basename='cart')




urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop/<int:pk>', ShopView.as_view(), name='shop_pk'),
    path('filtershop/', FilterShopView.as_view(), name='filter'),
    path('filtershop/<int:pk>', FilterShopView.as_view(), name='filter_pk'),
    path('product/<slug:slug>', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart' ),
    
    path('api/', include(router.urls)),
    path('api/prof/', ProfileAPIView.as_view()),
]
