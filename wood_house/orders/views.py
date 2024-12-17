from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from .models import Order, OrderItem


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginated_by = 10

    def get_queryset(self):
        queryset = Order.objects.select_related("user").order_by("-created_at")
        # Apply status filter
        status = self.request.GET.get("status")
        if status and status in dict(Order.STATUS_CHOICES):
            queryset = queryset.filter(status=status)
        # Aplly search
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Order.STATUS_CHOICES
        context["current_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("search", "")
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.select_related("user").prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product")
            )
        )
