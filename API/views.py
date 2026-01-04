from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from Home.models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CartSerializer, CartItemCreateSerializer, GuestCartSerializer
from .models import Cart, CartItem, GuestCart
from rest_framework import permissions
from .serializers import OrderSerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# List all products & create new ones
class ListCreateProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    
    def get_queryset(self):
        queryset = Product.objects.all().order_by('id')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('id')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Retrieve, update, or delete a single product
class RetrieveUpdateDestroyProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'uuid'


class AdminOrderList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orders = getattr(__import__('API.models', fromlist=['Order']), 'Order').objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Only authenticated users may create orders — use the user's cart
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart not found'}, status=status.HTTP_400_BAD_REQUEST)

        items = list(cart.items.select_related('product').all())

        if not items:
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        Order = getattr(__import__('API.models', fromlist=['Order']), 'Order')
        OrderItem = getattr(__import__('API.models', fromlist=['OrderItem']), 'OrderItem')

        # Create order
        order = Order.objects.create(
            user=user,
            status='P'
        )

        total = 0
        for it in items:
            prod = it.product
            price = prod.Price
            qty = it.quantity
            OrderItem.objects.create(
                order=order,
                product=prod,
                price=price,
                quantity=qty
            )
            total += float(price) * int(qty)

        order.total = total
        order.save()

        # Clear cart items
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Handle both authenticated users and guests
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)
            print(serializer.data)
            return Response(serializer.data)
        else:
            # Use guest_id from middleware
            guest_id = getattr(request, 'guest_id', None)
            if not guest_id:
                return Response({'detail': 'No guest_id found'}, status=status.HTTP_400_BAD_REQUEST)
            guest_cart, _ = GuestCart.objects.get_or_create(guest_id=guest_id)
            serializer = GuestCartSerializer(guest_cart)
            return Response(serializer.data)


class AddCartItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product_uuid']
        quantity = serializer.validated_data['quantity']

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, guest_cart=None, product=product,
                                                          defaults={'quantity': quantity})
            if not created:
                item.quantity = item.quantity + quantity
                item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        else:
            # Handle guest
            guest_id = getattr(request, 'guest_id', None)
            if not guest_id:
                return Response({'detail': 'No guest_id found'}, status=status.HTTP_400_BAD_REQUEST)
            guest_cart, _ = GuestCart.objects.get_or_create(guest_id=guest_id)
            item, created = CartItem.objects.get_or_create(guest_cart=guest_cart, cart=None, product=product,
                                                          defaults={'quantity': quantity})
            if not created:
                item.quantity = item.quantity + quantity
                item.save()
            return Response(GuestCartSerializer(guest_cart).data, status=status.HTTP_201_CREATED)


class CartItemDetail(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        if request.user.is_authenticated:
            try:
                item = CartItem.objects.get(pk=pk, cart__user=request.user)
            except CartItem.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            quantity = request.data.get('quantity')
            if quantity is not None:
                item.quantity = int(quantity)
                item.save()
            return Response(CartSerializer(item.cart).data)
        else:
            # Handle guest
            guest_id = getattr(request, 'guest_id', None)
            if not guest_id:
                return Response({'detail': 'No guest_id found'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                item = CartItem.objects.get(pk=pk, guest_cart__guest_id=guest_id)
            except CartItem.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            quantity = request.data.get('quantity')
            if quantity is not None:
                item.quantity = int(quantity)
                item.save()
            return Response(GuestCartSerializer(item.guest_cart).data)

    def delete(self, request, pk):
        if request.user.is_authenticated:
            try:
                item = CartItem.objects.get(pk=pk, cart__user=request.user)
            except CartItem.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            cart = item.cart
            item.delete()
            return Response(CartSerializer(cart).data, status=status.HTTP_204_NO_CONTENT)
        else:
            # Handle guest
            guest_id = getattr(request, 'guest_id', None)
            if not guest_id:
                return Response({'detail': 'No guest_id found'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                item = CartItem.objects.get(pk=pk, guest_cart__guest_id=guest_id)
            except CartItem.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            guest_cart = item.guest_cart
            item.delete()
            return Response(GuestCartSerializer(guest_cart).data, status=status.HTTP_204_NO_CONTENT)