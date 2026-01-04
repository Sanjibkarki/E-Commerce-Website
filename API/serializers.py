from rest_framework import serializers
from Home.models import Product
from .models import Cart, CartItem, GuestCart



class ProductSerializer(serializers.ModelSerializer):
    Image = serializers.ImageField(use_url=True, read_only=True)
    class Meta:
        model = Product
        fields = ['uuid', 'Image', 'Name', 'Description','Price', 'Quantity', 'category']



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']


class GuestCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = GuestCart
        fields = ['id', 'guest_id', 'items']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = getattr(__import__('API.models', fromlist=['OrderItem']), 'OrderItem')
        fields = ['id', 'product', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = getattr(__import__('API.models', fromlist=['Order']), 'Order')
        fields = ['id', 'user', 'guest_id', 'total', 'status', 'created_at', 'items']


class CartItemCreateSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_uuid(self, value):
        try:
            return Product.objects.get(uuid=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found')

    def create(self, validated_data):
        # not used directly
        pass
