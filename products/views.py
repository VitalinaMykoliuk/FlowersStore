from django.shortcuts import render
from django.views import View
from products.models import ProductCategory, Product


class MainPage(View):
    template_name = 'products/products.html'

    def get(self, request):
        return render(request, self.template_name)


class MainProductCategory(View):
    template_name = 'products/product_category.html'

    def get(self, request):
        all_category = ProductCategory.objects.all()
        return render(request, self.template_name, {'category': all_category})


class ProductCatalog(View):
    template_name = 'products/catalog_product.html'

    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id)
        return render(request, self.template_name, {'products': products})


class ContactPage(View):
    template_name = 'products/contacts.html'

    def get(self, request):
        return render(request, self.template_name)
