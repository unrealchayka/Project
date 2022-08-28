from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Brand, Cart, Category, Checkout, Comment, CustomUser,
                     Product, Rating, RatingStar, Tag)


class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('title','id','price', 'in_stock', 'get_photo')
    search_fields = ('title','pub_date')
    list_filter = ('title','pub_date','id')
    prepopulated_fields = {'slug' : ('title','category',)}

    def get_photo(self, object):
        if object.image:
            return mark_safe(f'<img src= {object.image.url} width=50 >')

    get_photo.short_description = 'Фото'


class CastomUserAdmin(admin.ModelAdmin):
    list_display = ('username','id', 'is_active', 'get_photo')
    search_fields = ('username','id')

    def get_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src= {object.photo.url} width=50 >')
            
    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug' : ('title',)}

    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug' : ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}


admin.site.register(CustomUser, CastomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Checkout)




admin.site.site_title = 'Интеренет магазин'
admin.site.site_header = 'Интеренет магазин'
