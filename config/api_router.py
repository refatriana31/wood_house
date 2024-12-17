from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wood_house.users.api.views import UserViewSet
from wood_house.products.api.views import CategoryViewSet, ProductViewSet
from wood_house.orders.api.views import OrderViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# User routes
router.register("users", UserViewSet)

# Product routes
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")

# Order routes
router.register("orders", OrderViewSet, basename="order")

app_name = "api"
urlpatterns = router.urls
