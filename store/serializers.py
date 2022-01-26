from rest_framework import serializers
from store.models import Cart, CartItem, Collection, Product, Review


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


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        return CartItem.objects.create(cart_id=self.context['cart_id'], **validated_data)


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity')
        instance.save()
        return instance
