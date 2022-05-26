from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name="store"),
    path('<slug:category_slug>', views.store, name='product_by_category'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    # path('products/', views.products, name="product"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

]
