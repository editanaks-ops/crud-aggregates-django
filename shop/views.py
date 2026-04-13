from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Avg, Min, Max, Count
from .models import Product, Category
from .forms import ProductForm, CategoryForm


def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Фильтрация
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # Сортировка
    sort = request.GET.get('sort')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'date_asc': 'created_at',
        'date_desc': '-created_at',
    }

    if sort in sort_options:
        products = products.order_by(sort_options[sort])

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'selected_sort': sort,
    }
    return render(request, 'shop/product_list.html', context)


def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'shop/create_product.html', {'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'shop/update_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/delete_product.html', {'product': product})


def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'shop/category_list.html', {'categories': categories})


def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'shop/create_category.html', {'form': form})


def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'shop/update_category.html', {'form': form, 'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'shop/delete_category.html', {'category': category})


def analytics_view(request):
    overall_stats = Product.objects.aggregate(
        total_products=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        min_price=Min('price'),
        max_price=Max('price'),
    )

    category_stats = Category.objects.annotate(
        product_count=Count('products'),
        total_price=Sum('products__price'),
        avg_price=Avg('products__price'),
        min_price=Min('products__price'),
        max_price=Max('products__price'),
    ).order_by('name')

    context = {
        'overall_stats': overall_stats,
        'category_stats': category_stats,
    }
    return render(request, 'shop/analytics.html', context)