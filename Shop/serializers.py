from email.policy import default
from urllib import request
from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'title', 'category')
    # owner = serializers.HiddenField(default = serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    # brand = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    # color = serializers.SlugRelatedField(slug_field='color', read_only=True)
    # tags = serializers.SlugRelatedField(slug_field='tags', read_only = True, many = True)
    # photo = serializers.SlugRelatedField(slug_field='photo', read_only =True)

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)

class DetailProductSerializer(serializers.ModelSerializer):
    

    # owner = serializers.SlugRelatedField(slug_field='username', read_only = True)
    # categories = serializers.SlugRelatedField(slug_field='name_categories', read_only=True)
    # brand = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    # tags = serializers.SlugRelatedField(slug_field='tags', read_only = True, many = True)
    # photo = serializers.SlugRelatedField(slug_field='photo', read_only =True)
    class Meta:
        model = Product
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    # user = serializers.SlugRelatedField(slug_field = 'username', read_only = True)
    # product = serializers.SlugRelatedField(slug_field='title', read_only = True)


    class Meta:
        model = Comment
        fields = ('user', 'product', 'text')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('user', 'product', 'star')

    def create(self, validated_data):
        rating, _= Rating.objects.update_or_create(
            user = validated_data.get('user', None),
            product = validated_data.get('product', None),
            defaults={'star' : validated_data.get('star')}
        )
        return rating


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):

    username = serializers.HiddenField(default = serializers.CurrentUserDefault())
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'social_network')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.social_network = validated_data.get('social_network', instance.social_network)
        instance.save()
        return instance
