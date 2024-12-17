from rest_framework import viewsets, filters
from django_filters import rest_framework as django_filters
from wood_house.products.models import Category, Product
from wood_house.products.api.serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer
)


class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id')
    min_price = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='lte')
    category_name = django_filters.CharFilter(field_name='category__name',
                                              lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(category__is_active=True)
    filterset_class = ProductFilter
    filter_backends = [django_filters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'price', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
