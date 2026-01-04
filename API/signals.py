from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Cart, CartItem, GuestCart
from Home.models import Product


User = get_user_model()


@receiver(post_save, sender=User)
def merge_guest_cart_on_login(sender, instance, created, **kwargs):
    """
    When a user logs in, merge their guest cart (if any) with their user cart.
    This signal is triggered when a user object is saved (which happens on login).
    We detect login by checking the user session for guest_id and merging if present.
    """
    # This is called whenever a User is saved. We need to merge guest carts
    # after user authentication. This is better handled via post_login signal.
    # For now, we'll handle it in a login view or middleware.
    pass


def merge_guest_cart_to_user(user, guest_id):
    """
    Merge guest cart items into user cart.
    Called after user authentication.
    """
    try:
        guest_cart = GuestCart.objects.get(guest_id=guest_id)
    except GuestCart.DoesNotExist:
        return

    # Get or create user cart
    user_cart, _ = Cart.objects.get_or_create(user=user)

    # Merge items
    for guest_item in guest_cart.items.all():
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=guest_item.product,
            defaults={'quantity': guest_item.quantity}
        )
        if not created:
            # Item already exists, add quantities
            user_item.quantity += guest_item.quantity
            user_item.save()

    # Delete guest cart after merging
    guest_cart.delete()
