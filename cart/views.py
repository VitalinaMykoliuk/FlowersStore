import json

from django.shortcuts import render, redirect
from django.views import View
from cart.models import CartItem
from django.contrib.sessions.models import Session
from products.models import Product
from django.http import JsonResponse
from orders.models import Order


class CartUser(View):
    template_name = 'cart/basket.html'

    def get(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            print(f'$$${request.session.session_key}')
            cart_item_ids = request.session.get('cart_item_ids', [])
            print(cart_item_ids)
            cart_items = CartItem.objects.filter(id__in=cart_item_ids)
            print(cart_items)
        return render(request, self.template_name, {'cart_items': cart_items})


class AddToCart(View):

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)  #получаем обьект продукта с б/д
        if request.user.is_authenticated: #проверяем аутентифицирован ли пользователь
            cart, created = CartItem.objects.get_or_create(user=request.user, product=product)
            #получаем объект CartItem для данного пользователя и продукта. Если такого объекта еще нет, он создается
            if not created:
                cart.quantity += 1
                cart.save()
            #Если объект CartItem уже существует,то увеличивается его количество на единицу и сохраняются изменения.
        else:
            cart_item_ids = request.session.get('cart_item_ids', [])
            print(cart_item_ids)
            #эта строка извлекает список идентификаторов товаров из сессии пользователя
            cart_item = CartItem.objects.filter(product=product, id__in=cart_item_ids).first()
            print(cart_item)
            #Эта строка пытается найти объект CartItem, соответствующий продукту и присутствующему
            # списку идентификаторов товаров.
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
            #Если объект CartItem уже существует для данного товара, то увеличивается
            # его количество на единицу и сохраняются изменения.
            else:
                cart_item = CartItem.objects.create(product=product, quantity=1)
                print(cart_item)
                cart_item_ids.append(cart_item.id)
                request.session['cart_item_ids'] = cart_item_ids
                request.session.modified = True
            #Если объект CartItem не найден, то создается новый объект с количеством равным 1.
            # Затем идентификатор этого объекта добавляется в список cart_item_ids, который сохраняется
            # в сессии пользователя. Затем устанавливается флаг modified, чтобы указать, что сессия была изменена.
        return redirect('user_basket')
        #перенаправление пользователя на страницу корзины


class RemoveFromCart(View):
    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, product=product).first()
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
        else:
            cart_item_ids = request.session.get('cart_item_ids', [])
            cart_item = CartItem.objects.filter(product=product, id__in=cart_item_ids).first()
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item_ids.remove(cart_item.id)
                    request.session['cart_item_ids'] = cart_item_ids
                    request.session.modified = True
        return redirect('user_basket')


class Checkout(View):
    template_name = 'cart/create_order.html'

    def get(self, request):
        return render(request, self.template_name)


class SuccessPage(View):
    template_name = 'cart/success.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form_data = request.POST
        cart_user = request.user
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=cart_user)
            order = Order(
                first_name=form_data['name'],
                email=form_data['email'],
                address=form_data['address'],
                initiator=cart_user
            )
            order.update_after_payment(cart_user)
            order.save()
            cart_items.delete()
        else:
            cart_item_ids = request.session.get('cart_item_ids', [])
            print(f'item {cart_item_ids}')
            cart_items = CartItem.objects.filter(id__in=cart_item_ids)
            dict_product = {}
            for item in cart_items:
                name_product = item.product.name
                price_product = item.product.price
                dict_product[name_product] = price_product
            dict_serializable = {str(key): str(value) for key, value in dict_product.items()}
            json_string = json.dumps(dict_serializable)
            order = Order(
                first_name=form_data['name'],
                email=form_data['email'],
                address=form_data['address'],
                basket_history=json_string,
            )
            order.save()
            dict_product.clear()
            cart_items.delete()
            del request.session['cart_item_ids']
            request.session.modified = True
        return render(request, self.template_name)


