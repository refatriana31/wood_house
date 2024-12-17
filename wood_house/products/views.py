from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from wood_house.products.models import Product
from wood_house.products.forms import ProductForm, ProductFilterForm


# Product List View
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Show 10 products per page

    def get_queryset(self):
        # Get all products ordered by created_at (newest first)
        queryset = Product.objects.all().order_by('-created_at')
        # Filter by category if provided in the request
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        # Filter by search query if provided in the request
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilterForm()  # Add filter form to context
        return context


# Product Detail View
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'products'


# Product Delete View
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


# Product Create View
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product:product_list')


# Product Update View
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product:product_list')


# Instantiate all views
productlistview = ProductListView.as_view()
productdetailview = ProductDetailView.as_view()
productdeleteview = ProductDeleteView.as_view()
productcreateview = ProductCreateView.as_view()
productupdateview = ProductUpdateView.as_view()
