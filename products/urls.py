from django.urls import path
from .views import MainPage, MainProductCategory, ProductCatalog, ContactPage

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('product_category/', MainProductCategory.as_view(), name='product_cat'),
    path('products/<int:category_id>/', ProductCatalog.as_view(), name='product_list'),
    path('contacts/', ContactPage.as_view(), name='contact_store'),
]