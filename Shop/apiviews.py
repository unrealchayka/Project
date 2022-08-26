from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import *


from .models import *
from .serializers import *
from .service import *


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


class ProductViewSet(ReadOnlyModelViewSet):
    '''Список товаров и подробное описание'''

    queryset = Product.objects.all()
    filterset_fields = ['title']
    pagination_class = ProductPage

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'retrive':
            return DetailProductSerializer

class CommentAPIView(ModelViewSet):
    '''Комментарии к товару'''
 
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CastomPage


class AddStarRatingViewSet(ModelViewSet):

    queryset = Rating.objects.all()
    filterset_fields = ['user', 'product']
    serializer_class = RatingSerializer


# class DetailProductAPIView(generics.RetrieveUpdateAPIView):
#     '''Подробное описание товара'''
#     queryset = Product.objects.all()
#     # permission_classes = (permissions.IsAdminUser,)
#     serializer_class = DetailProductSerializer


# class UpdateDestroyProductAPIView(generics.RetrieveUpdateDestroyAPIView):
#     '''Редактирование товара'''

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (permissions.IsAdminUser,)

# class ListCartAPIView(APIView):
#     '''Корзина'''
#     serializer_class = CartSerializer
    
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, *args, **kwargs):
#         cart = Cart.objects.filter(user_id = self.request.user.id)
#         return Response ({'get' : CartSerializer(cart, many = True).data})

#     def post(self, request):
#         serializer = CartSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response ({'post' : serializer.data})

# class UpdateDestroyCartAPIView(APIView):
    
#     def get(self, request, *args, **kwargs):
#         cart = Cart.objects.get(id = self.kwargs['pk'])
#         return Response({'get' : CartSerializer(cart).data})

#     def put(self, request, *args, **kwargs):
#         pk = self.kwargs['pk']
#         try:
#             instance = Cart.objects.get(id = pk)
#         except:
#             return Response({'error': 'Objects not exist'})

#         serializers = CartSerializer(data = request.data, instance = instance)
#         serializers.is_valid(raise_exception = True)
#         serializers.save()
#         return Response({'put' : serializers.data})
    
#     def delete(self, request, *args, **kargs):
#         pk = self.kwargs.get('pk')
#         try:
#             Product.objects.delete(pk=pk)
#         except:
#             return Response({'error' : 'Object does not exist'})
#         return Response({'delete': f'object {pk} delete'}) 



# class UserListView(generics.ListAPIView):

#     queryset = CastomUser.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [DjangoFilterBackend]



        

# class ProductAPIList(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductCreateAPI(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (permissions.IsAdminUser,)

# class ProductAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (permissions.IsAdminUser,)

# class ProductAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (permissions.IsAdminUser,)



# class PoductListAPIView(APIView):
#     # queryset = Product.objects.all()

#     def get(self, request):
#         product = Product.objects.all()
#         return Response(ProductSerializer(product, many = True).data)

#     def post(self, request):
#         ser = ProductSerializer(data = request.data)
#         ser.is_valid(raise_exception = True)
#         ser.save()
#         return Response({'post': ser.data})

#     def put(self, request, *args, **kargs):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Response({'error' : 'Method PUT not allowed'})
#         try:
#             instance = Product.objects.get(pk=pk)
#         except:
#             return Response({'error' : 'Object does not exist'})

#         serializer = ProductSerializer(data = request.data, instance = instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post' : serializer.data})

#     def delete(self, request, *args, **kargs):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Response({'error' : 'Method delete not allowed'})
#         try:
#             Product.objects.delete(pk=pk)
#         except:
#             return Response({'error' : 'Object does not exist'})
#         return Response({'post': 'post delete' + str(pk)})




# class ProductDetailView(APIView):
#     queryset = Products_name.objects.all()
#     def get(self, request, slug):
#         product = Products_name.objects.get(slug = slug)
#         serializer = ProductDetailSerializer(product)
#         return Response({'get':serializer.data})

# class ProductAddView(APIView):
#     queryset = Products_name.objects.all()
#     def post(self, request):
#         product = ProductAddSerializer(data = request.data)
#         if product.is_valid():
#             product.save()
#         return Response(status=201)
