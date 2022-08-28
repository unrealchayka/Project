from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


def get_client_ip(request):
    x_forwardet_for = request.META.get('X_FORWARDED_FOR')
    if x_forwardet_for:
        ip = x_forwardet_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_staff


class ProductPage(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CustomPage(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000
    
