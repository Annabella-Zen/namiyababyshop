# from asyncio.windows_events import NULL
from django.shortcuts import redirect, render, get_object_or_404
from cart.cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST
from cart.models import Order, OrderItem
from customer.models import KhachHang


# Create your views here.
def checkout(request):
    cart = Cart(request)

    # đặt hàng
    if request.POST.get('btnDatHang'):
        khach_hang = KhachHang.objects.get_or_create(email=request.POST.get('email'))
        # if khach_hang.ten == NULL:
        #     khach_hang.ten = request.POST.get('ten')
        # if khach_hang.dien_thoai == NULL:
        #     khach_hang.dien_thoai = request.POST.get('dien_thoai')
        #     khach_hang.dia_chi = request.POST.get('dia_chi')
        #     khach_hang.save()
        order = Order()

        # Gán giá trị
        order.username = request.POST.get('email')
        order.first_name = request.POST.get('ten')
        order.phone = request.POST.get('dien_thoai')
        order.address = request.POST.get('dia_chi')
        order.note = request.POST.get('note')
        order.total = cart.get_final_total_price()
        order.save()

        for c in cart:
            OrderItem.objects.create(order=order,
                                        product=c['product'],
                                        price=c['price'],
                                        quantity=c['quantity']
                                        )

        cart.clear()

        return render(request, 'store/result.html', {
        'cart': cart,
        })

    return render(request, 'store/checkout.html', {
        'cart': cart,
    })


def cart_detail(request):
    cart = Cart(request)

    # Sử dụng mã giảm giá
    chuoi_kq = ''
    if request.POST.get('btnCoupon'):
        # Gán biến
        coupon_code = request.POST.get('coupon_code')
        if coupon_code == 'SALE':
            cart_new = {}
            for c in cart:
                product = c['product']
                product_cart = {
                    str(product.pk): {
                        'quantity': c['quantity'], 
                        'price': str(product.price), 
                        'coupon': '0.9'
                        }
                    }
                cart_new.update(product_cart)  # Cập nhật vào dict cart_new để lưu vào session
                c['coupon'] = 0.9  # Cập nhật tỉ lệ giảm giá để giữ lại trên session

            request.session['cart'] = cart_new
        else:
            chuoi_kq = 'Mã không hợp lệ.'


    # Cập nhật giỏ hàng
    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for c in cart:
            product = c['product']
            quantity_new = int(request.POST.get('quantity-final-' + str(product.pk)))
            if quantity_new != 0:
                product_cart = {
                    str(product.pk): {
                        'quantity': quantity_new, 
                        'price': str(product.price), 
                        'coupon': str(c['coupon'])
                        }
                    }
                cart_new.update(product_cart)  # Cập nhật vào dict cart_new để lưu vào session
                c['quantity'] = quantity_new  # Cập nhật số lượng để giữ lại trên giao diện giỏ hàng
            else:
                cart.remove(product)

        request.session['cart'] = cart_new  # Lưu vào session

    return render(request, 'store/cart.html', {
        'cart': cart,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product=product, quantity=int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:cart_detail')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        print("Add success")
        cart.add(product=product, quantity=int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')