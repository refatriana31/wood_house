from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wood_house.orders.models import Order
from wood_house.orders.api.serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer
)
from django.db import transaction

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk Order dengan endpoints:
    - POST /api/orders/ (create order)
    - GET /api/orders/ (list user orders)
    - GET /api/orders/{id}/ (order detail)
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']  # Batasi hanya GET dan POST

    def get_queryset(self):
        """
        Return orders for the authenticated user only.
        """
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Use different serializers based on the action.
        """
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer

    def perform_create(self, serializer):
        """
        Create an order with related items for the authenticated user.
        """
        with transaction.atomic():
            serializer.save(user=self.request.user)
