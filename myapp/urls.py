from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.landpage,name='landpage'),
    path('front',views.front,name='front'),
    path('login',views.login,name='login'),
    path('adregister',views.adregister,name='adregister'),
    path('logout',views.logout,name='logout'),

    path('api/stock/', views.api_stock),
    path('api/orders/', views.api_orders),
    path('api/users/', views.api_users),
    path('api/delete-product/<int:id>/', views.api_delete_product),
    path('update-status/<int:order_id>/', views.update_status, name='update_status'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('api/update-product/<int:id>/', views.product_update, name='update_product'),
    path('api/stock/<int:id>/', views.single_product, name='single_product'),
    path("api/admin-reports/", views.admin_reports, name="admin_reports"),

    path('user_profile', views.user_profile, name='user_profile'),
    path("place-order", views.place_order, name="place_order"),
    path('place-prescription', views.place_prescription, name='place_prescription'),
    path('check-product-type', views.check_product_type, name='check_product_type'),
    path("get_cart_items/", views.get_cart_items, name="get_cart_items"),
    path('get-orders-ajax/', views.get_orders_ajax, name='get_orders_ajax'),
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path('home', views.home, name="home"),
    path('search-medicines/', views.search_medicines, name='search_medicines'),
    path("submit-report/", views.submit_report, name="submit_report"),

    path("update-cart-quantity/", views.update_cart_quantity, name="update_cart_quantity"),
    path("delete-cart-item/", views.delete_cart_item),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
