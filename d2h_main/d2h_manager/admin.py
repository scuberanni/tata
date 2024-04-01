from django.contrib import admin
from.models import product_master,retailer_master,box_master,product,box_product,box_retailer_master
from.models import to_ret_product,sale_product,sale_to_ret_product
# Register your models here.
admin.site.register(product_master)
admin.site.register(retailer_master)
admin.site.register(box_master)
admin.site.register(product)
admin.site.register(to_ret_product)
admin.site.register(box_product)
admin.site.register(box_retailer_master)
admin.site.register(sale_product)
admin.site.register(sale_to_ret_product)