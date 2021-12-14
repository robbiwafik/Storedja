from re import MULTILINE
from rest_framework import serializers
from store.models import Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    products = serializers.SerializerMethodField()

    def get_products(self, collection: Collection):
        return collection.products.count()


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, coerce_to_string=False)
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )
