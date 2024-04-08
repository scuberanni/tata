from django.urls import path 
from . import views


urlpatterns = [

    path('',views.home,name='home'),
    path('admin/',views.admin,name='admin'),
    path('search',views.search,name='search'),
    path('pr_master/',views.pr_master,name='pr_master'),
    path('bo_master/',views.bo_master,name='bo_master'),
    path('add_box_master',views.add_box_master,name='add_box_master'),
    path('close_box_master',views.close_box_master,name='close_box_master'),
    path('stock_view',views.stock_view,name='stock_view'),
    path('stock_view_ret,<pk>',views.stock_view_ret,name='stock_view_ret'),
    path('stock_view_all',views.stock_view_all,name='stock_view_all'),
    path('detail_view',views.detail_view,name='detail_view'),
    path('ret_master/',views.ret_master,name='ret_master'),
    path('master',views.master,name='master'),
    path('box_edit,<pk>',views.box_edit,name='box_edit'),
    path('box_dlt,<pk>',views.box_dlt,name='box_dlt'),
    path('product_edit,<pk>',views.product_edit,name='product_edit'),
    path('product_dlt,<pk>',views.product_dlt,name='product_dlt'),
    path('retailer_edit,<pk>',views.retailer_edit,name='retailer_edit'),
    path('retailer_edit1,<pk>',views.retailer_edit1,name='retailer_edit1'),
    path('retailer_dlt,<pk>',views.retailer_dlt,name='retailer_dlt'),
    path('box_details_edit,<pk>',views.box_details_edit,name='box_details_edit'),
    path('woc,<pk>',views.woc,name='woc'),
    path('box_details_delete,<pk>',views.box_details_delete,name='box_details_delete'),
    path('add_product',views.add_product,name='add_product'),
    path('ret_product',views.ret_product,name='ret_product'),
    path('ret_home',views.ret_home,name='ret_home'),
    path('ret_kan',views.ret_kan,name='ret_kan'),
    path('ret_ret',views.ret_ret,name='ret_ret'),
    path('sale_ret_product',views.sale_ret_product,name='sale_ret_product'),
    path('sale_ret_kan',views.sale_ret_kan,name='sale_ret_kan'),
    path('sales_reports',views.sales_reports,name='sales_reports'),
    path('adjust_box',views.adjust_box,name='adjust_box'),

]