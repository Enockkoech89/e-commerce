from django.contrib import admin

# Register your models here.
from .models import Item, OrderItem, Order, BillingAddress, Payment, Profile, Free, Sinema

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Profile)
admin.site.register(Free)
admin.site.register(Sinema)

