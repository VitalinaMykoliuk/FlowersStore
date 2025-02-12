from django.urls import path
from cart.views import CartUser, AddToCart, RemoveFromCart, Checkout, SuccessPage


urlpatterns = [
    path('basket/', CartUser.as_view(), name='user_basket'),
    path('add_to_cart/<int:product_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('remove_to_cart/<int:product_id>/', RemoveFromCart.as_view(), name='remove_to_cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('success/', SuccessPage.as_view(), name='success_to_order'),

]