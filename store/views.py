from functools import partial
from django.db.models.base import Model
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from store.filters import ProductFilter
from .models import Collection, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['description', 'title', 'collection__title']

    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with order items'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {'request': self.request}


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('products').all()
    serializer_class = CollectionSerializer

    def destroy(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with other products'}, status=status.HTTP_403_FORBIDDEN)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
