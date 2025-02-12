import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

# class DataIntoOrdersName(View):
#
#     def post(self):

class UserOrder(View):
    template_name = 'orders/user_order.html'

    def get(self, request):
        return render(request, self.template_name)


class SuccessToOrderView(View):
    template_name = 'orders/payment.html'

    def get(self, request):
        return render(request, self.template_name)



