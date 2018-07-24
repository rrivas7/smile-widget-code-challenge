from django.db import models
from django.db.models import Q


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)

    def price_on_date(self, date):
        product_price = self.productprice_set.filter(Q(date_start__lte=date) | Q(date_start=None)).filter(Q(date_end__gte=date) | Q(date_end=None)).first()
        if product_price:
            return product_price.price
        else:
            return self.price

class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)

class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    price = models.PositiveIntegerField(help_text='Price of product in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
