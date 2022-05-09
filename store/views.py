from django.shortcuts import render, redirect, reverse, get_object_or_404
from store.models import SubCategory, Product, SubCategoryLevel2
from django.core.paginator import Paginator
from cart.cart import Cart
from store.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer
from urllib.parse import urlencode
# Create your views here.


def products_service(request):
    products = Product.objects.order_by('-public_day')
    result_list = list(products.values('name', 'price', 'image', 'public_day'))
    return JsonResponse(result_list, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-public_day')
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser]  # Đọc / Ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Chỉ đọc


def product_service(request, pk):
    products = Product.objects.filter(pk=pk).order_by('-public_day').count()
    result_list = list(products.values('name', 'price', 'image', 'public_day'))[0]
    return JsonResponse(result_list, safe=False)
    


def index(request):
    
    cart = Cart(request)
    sub_category = SubCategory.objects
    all_products = Product.objects.all()

    # Baby Items
    be_products = Product.objects.filter(category_id=1).order_by('-public_day').all()
    beuong_items = list(SubCategoryLevel2.objects.filter(subcategory=1).values_list('id', 'name'))
    bemac_items = list(SubCategoryLevel2.objects.filter(subcategory=2).values_list('id', 'name'))
    bevesinh_items = list(SubCategoryLevel2.objects.filter(subcategory=3).values_list('id', 'name'))

    # Mom Items
    me_products = Product.objects.filter(category_id=2).order_by('-public_day')
    medep_items = list(SubCategoryLevel2.objects.filter(subcategory=5).values_list('id', 'name'))
    mekhoe_items = list(SubCategoryLevel2.objects.filter(subcategory=6).values_list('id', 'name'))
    mebau_items = list(SubCategoryLevel2.objects.filter(subcategory=4).values_list('id', 'name'))

    # Home
    # home_subcategory = SubCategory.objects.filter(category=2).values_list('id')
    # home_list_subcategory = []
    # for subcategory in home_subcategory:
    #     home_list_subcategory.append(subcategory[0])
    # home_products = Product.objects.filter(subcategory__in=home_list_subcategory).order_by('-public_day')



    return render(request, 'store/index.html', {
        'sub_category': sub_category,
        'all_products': all_products[:15],
        'be_products': be_products[:21],
        'me_products': me_products[:21],

        'beuong_items': beuong_items[:21],
        'bemac_items': bemac_items[:21],
        'bevesinh_items': bevesinh_items[:21],

        'medep_items': medep_items[:21],
        'mekhoe_items': mekhoe_items[:21],
        'mebau_items': mebau_items[:21],

        'cart': cart
    })


def get_baby_sub_category_2(sub_category_id):
    baby_sub_category2 = SubCategoryLevel2.objects.filter(subcategory_id=sub_category_id).values_list('id', 'name')
    return JsonResponse(baby_sub_category2, safe=False)


def subcategory(request, pk):
    cart = Cart(request)

    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory = SubCategory.objects.order_by('name')
    

    # Đọc danh sách sản phẩm theo danh mục
    if pk == 0:
        products = Product.objects.order_by('-public_day')
        subcategory_name = 'Tất cả sản phẩm (' + str(len(products)) + ')'
    else:
        products = Product.objects.filter(category=pk).order_by('-public_day')
        selected_subcategory = SubCategory.objects.get(pk=pk)
        subcategory_name = selected_subcategory.name + ' (' + str(len(products)) + ')'
        


    # Lọc giá
    from_price = ''
    to_price = ''
    if request.GET.get('from_price'):
        # Gán biến
        from_price = int(float(request.GET.get('from_price')))
        to_price = int(float(request.GET.get('to_price')))

        products = [product for product in products if from_price <= product.price <= to_price]  
        subcategory_name = '%i sản phẩm được tìm thấy trong khoảng %i - %i' % (len(products), from_price, to_price)



    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html', {
        'list_subcategory': list_subcategory,
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'cart': cart,
        
        'from_price': from_price,
        'to_price': to_price,
    })



def subcategory2(request, pk):
    cart = Cart(request)

    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory2 = SubCategoryLevel2.objects.order_by('name')
    
    # Đọc danh sách sản phẩm theo danh mục
    if pk == 0:
        products = Product.objects.order_by('-public_day')
        subcategory_name = 'Tất cả sản phẩm (' + str(len(products)) + ')'
    else:
        products = Product.objects.filter(subcategorylevel2_id=pk).order_by('-public_day')
        selected_subcategory2 = SubCategoryLevel2.objects.get(pk=pk)
        subcategory_name = selected_subcategory2.name + ' (' + str(len(products)) + ')'

    # Lọc giá
    from_price = ''
    to_price = ''
    if request.GET.get('from_price'):
        # Gán biến
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))

        # if product_name != '':
        #     products = Product.objects.filter(name__contains=product_name).order_by('price')

        products = [product for product in products if from_price <= product.price <= to_price]  # List comprehension
        subcategory_name = '%i sản phẩm được tìm thấy trong khoảng %s - %s' % (len(products), "{:,}".format(from_price), "{:,}".format(to_price))


    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html', {
        'list_subcategory2': list_subcategory2,
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'cart': cart,
        'from_price': from_price,
        'to_price': to_price,
        'pk': pk,
        'soluong_tong': str(len(products)),
        'soluong_tren_page':str(len(products_pager)),
    })





def contact(request):
    cart = Cart(request)

    return render(request, 'store/contact.html', {
        'cart': cart,
    })

def blog(request):

    return render(request, 'store/blog.html')

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'store/product-detail.html', {
#         'product': product,
#     })

def product_detail(request, product_id):
    cart = Cart(request)

    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory = SubCategory.objects.order_by('name')

    # Sản phẩm
    product = Product.objects.get(pk=product_id)

    # Subcategory
    subcategorylevel2_id = product.subcategorylevel2_id
    related_products = Product.objects.filter(subcategorylevel2_id=subcategorylevel2_id).exclude(id=product_id).order_by('public_day')

    # Subcategory name
    subcategory2name = SubCategoryLevel2.objects.get(pk=subcategorylevel2_id)

    return render(request, 'store/product-detail.html', {
        'cart': cart,
        'list_subcategory': list_subcategory,
        'product': product,
        'related_products': related_products,
        'subcategory2_id': subcategorylevel2_id,
        'subcategory2name': subcategory2name,
    })


def search(request):
    cart = Cart(request)

    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory2 = SubCategoryLevel2.objects.order_by('name')

    # Tìm kiếm
    products = []
    # result_search = ''
    if request.GET.get('condition'):
        
        keyword = request.GET.get('condition').strip()
        products = Product.objects.filter(name__contains=keyword).order_by('-public_day')
        #result_search = '%i sản phẩm với từ khóa "%s"' % (len(products), keyword)
        subcategory_name = 'Số sản phẩm tìm thấy (' + str(len(products)) + ')'
        # Phân trang
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 15)
        products_pager = paginator.page(page)
    
    return render(request, 'store/product-list.html', {
        'list_subcategory2': list_subcategory2,
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'cart': cart,
        'soluong_tong': str(len(products)),
        'soluong_tren_page':str(len(products_pager)),
        'pk': 0,
    })
