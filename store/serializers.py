from django.db.models import fields
from rest_framework import serializers
from store.models import Collection, Product, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.SerializerMethodField(read_only=True)

    def get_products_count(self, collection: Collection):
        return collection.products.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug',
                  'unit_price', 'inventory', 'collection']

    collection = serializers.HyperlinkedRelatedField(
        view_name='collection-detail',
        queryset=Collection.objects.all()
    )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
