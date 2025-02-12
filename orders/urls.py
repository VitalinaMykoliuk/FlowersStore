from django.urls import path
from orders.views import UserOrder, SuccessToOrderView


urlpatterns = [
    path('user_order/', UserOrder.as_view(), name='orders'),
    path('user_payment/', SuccessToOrderView.as_view(), name='payment'),

]