from rest_framework import serializers
from wood_house.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'get_item_total']
        read_only_fields = ['price', 'get_item_total']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'items']
        read_only_fields = ['total', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            # Check if product has enough stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for product {product.name}. Available: {product.stock}"
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            # Update product stock
            product.stock -= quantity
            product.save()
        return order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'status', 'created_at']
        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'user_username',
            'total', 'status', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = fields
