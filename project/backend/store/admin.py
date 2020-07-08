from django.contrib import admin
from store.models import Provider, Consumer, Category, Product, Store, Order, OrderProduct

class ProviderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Provider, ProviderAdmin)

class ConsumerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Consumer, ConsumerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)

class StoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Store, StoreAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)

class OrderProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderProduct, OrderProductAdmin)