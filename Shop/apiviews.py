from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import *

from .models import Comment, CustomUser, Product, Rating
from .serializers import (Cart, CartSerializer, CommentSerializer,
                          DetailProductSerializer, ProductSerializer,
                          RatingSerializer, UserSerializer)
from .service import CustomPage, ProductPage


class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):    
        user = CustomUser.objects.get(id = request.user.id)
        return Response({'get': UserSerializer(user).data})

    def patch(self, request):
        try:
            instance = CustomUser.objects.get(id = request.user.id)
        except:
            return Response({'error': 'user not exist'})

        serializers = UserSerializer(data = request.data, instance = instance, context = {'request' : request})
        serializers.is_valid(raise_exception = True)
        serializers.save()
        return Response({'put' : serializers.data})


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    '''Список товаров и подробное описание'''
    queryset = Product.objects.all()
    filterset_fields = ['title']
    pagination_class = ProductPage

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return ProductSerializer
        else:
            return DetailProductSerializer

class CommentAPIView(ModelViewSet):
    '''Комментарии к товару'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPage


class AddStarRatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    filterset_fields = ['user', 'product']
    serializer_class = RatingSerializer


class CartApiView(ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user.id)