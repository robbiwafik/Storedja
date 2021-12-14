from re import MULTILINE
from rest_framework import serializers
from store.models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.SerializerMethodField()

    def get_products_count(self, collection: Collection):
        return collection.products.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'collection']

    collection = serializers.HyperlinkedRelatedField(
        view_name='collection-detail',
        queryset=Collection.objects.all()
    )