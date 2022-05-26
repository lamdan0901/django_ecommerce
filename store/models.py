from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# *All classes inherit from models.Model

# 'class Customer'
# 'on_delete=models.CASCADE' means if the user is deleted,
# ...customer and all the orders associated with that user will be deleted as well

# 'class Product'
# 'digital products' are products that are not physical products, then cannot be shipped
# ***We have to install 'Pillow': a lib that processes images

# 'class Order'
# 'customer = models.ForeignKey(Customer,..' means that Customer is the foreign key
# ...to the Order class --> a customer can have many orders
# 'on_delete=models.SET_NULL' means that if the customer is deleted,
# ...the order will be set to null
# 'complete' means that the order is complete, it's False by default
# 'str(self.id)' converts the id to a string

# 'class OrderItem': one order can have many order items,
# ...each order item has a relationship with product

# 'class ShippingAddress'


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

    @property  # this is a property that helps us to get the image url
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, ])


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):  # check if the order has un-digital products or not, if true then display shipping address
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
