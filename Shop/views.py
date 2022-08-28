from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import CartForm, CastomUserForm, RatingForm
from .models import Cart, Comment, CustomUser, Product, Rating


class ProfileView(View):
    '''Личный кабинет пользователя'''
    def get(self, request):
        profile = CustomUser.objects.get(id = request.user.id)
        form = CastomUserForm(instance = request.user)
        return render(request, 'Shop/Profile.html', locals())

    def post(self, request):
        form = CastomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
            else:
                photo = form.instance.photo
            CustomUser.objects.update_or_create(
            id = request.user.id,
            defaults={
                'email': request.POST.get('email'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'social_network': request.POST.get('social_network'),
                'photo': photo,
            })
            return redirect('profile')
        else:
            form = CastomUserForm()
        return render(request, 'Shop/Profile.html', locals())


class CartView(View):
    '''Корзина'''
    def get(self, request):
        cart = Cart.objects.filter(user_id = request.user.id)
        return render(request, 'Shop/Cart.html', locals())


class AddCart(View):
    '''Добавление товара в корзину'''
    def post(self, request, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        Cart.objects.get_or_create(products=product, user_id=request.user.id, defaults={'quantit':kwargs['quantit']})


class DelCart(View):
    '''Удаление товара из корзины'''
    def post(self, request, **kwargs):
        cart = get_object_or_404(Cart, products_id=self.kwargs['pk'], user_id=request.user.id)
        cart.delete()


class HomeView(View):
    '''Домашняя страница'''
    def get(self, request):
        product = Product.objects.filter(in_stock = True)
        return render(request, 'Shop/Home.html', locals())
        

class ProductView(View):
    ''''Подробное описание товара'''
    def get(self, request, slug):
        product = Product.objects.select_related('category', 'brand',).get(slug = slug)
        comment = Comment.objects.filter(product__slug = slug).select_related('user', 'product')
        rating = RatingForm()
        cart = CartForm()
        return render(request, 'Shop/Product.html', locals())


class ShopView(View):
    '''Список товаров и фильтрация'''
    def get(self, request, pk = None):
        product  = Product.objects.all()
        if pk == 1:
            newest = datetime.now() - timedelta(minutes = 60 * 24 * 7)
            product = product.filter(create__gte = newest)

        return render(request, 'Shop/Shop.html', locals())


class AddRating(View):
    '''Добавление и изменение рейтинга к товару'''
    def post(self, requset, **kwargs):
        Rating.objects.get_or_create(
            user_id=requset.user.id, product_id=kwargs['pk'],
            defaults={'star':requset.POST.get('star')})
        


class FilterShopView(View):
    '''Фильтрация товаров'''
    def get(self, request, pk = None):
        product  = Product.objects.filter(
            Q(categories = request.GET.get('categories'))| 
            Q(brand = request.GET.get('brand'))|
            Q(price = request.GET.get('price')))
        if pk == 1:
            newest = datetime.now() - timedelta(minutes = 60 * 24 * 7)
            product = product.filter(create__gte = newest)
        return render (request, 'Shop/Shop.html', locals())
