from django.urls import path
from wood_house.products.views import (
    productlistview,
    productdetailview,
    productcreateview,
    productupdateview,
    productdeleteview
)

app_name = 'products'
urlpatterns = [
    path("", view=productlistview, name="product_list"),
    path("<int:pk>/", view=productdetailview, name="product_detail"),
    path("<int:pk>/delete/", view=productdeleteview, name="product_delete"),
    path("create/", view=productcreateview, name="product_create"),
    path("<int:pk>/update/", view=productupdateview, name="product_update"),

]
