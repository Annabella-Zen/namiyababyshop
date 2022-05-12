import email
from django.shortcuts import render, redirect
from customer.forms import FormDangKy, FormDoiMatKhau
from customer.models import KhachHang
from cart.cart import Cart
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher


# Create your views here.
def customer_login_signup(request):
    # Giỏ hàng
    cart = Cart(request)

    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_khach_hang' in request.session:
        return redirect('store:index')

    # ĐĂNG KÝ
    frm_dang_ky = FormDangKy()
    chuoi_kq_dang_ky = ''
    if request.POST.get('btnDangKy'):
        frm_dang_ky = FormDangKy(request.POST, KhachHang)
        if frm_dang_ky.is_valid() and frm_dang_ky.cleaned_data['mat_khau'] == frm_dang_ky.cleaned_data['xac_nhan_mat_khau']:
            # hasher = PBKDF2PasswordHasher() # salt: 1 byte
            hasher = Argon2PasswordHasher() # salt: 8 bytes
            request.POST.__mutable = True
            post = frm_dang_ky.save(commit=False)
            post.email = frm_dang_ky.cleaned_data['email']
            if KhachHang.objects.filter(email=post.email).exists():
                chuoi_kq_dang_ky = '''
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Email đã tồn tại trong hệ thống. Vui lòng đăng nhập!
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                '''
            else:
                post.mat_khau = hasher.encode(frm_dang_ky.cleaned_data['mat_khau'], '12345678')
                post.save()
                chuoi_kq_dang_ky = '''
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        Đã đăng ký thông tin thành công.
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                '''

    # ĐĂNG NHẬP
    chuoi_kq_dang_nhap = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        # Đọc dữ liệu từ CSDL
        khach_hang = KhachHang.objects.filter(email=email, mat_khau=encoded)

        if khach_hang.count() > 0:
            # Tạo session
            request.session['s_khach_hang'] = khach_hang.values()[0]  

            return redirect('store:index')
        else:
            chuoi_kq_dang_nhap = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng nhập không thành công. Vui lòng kiểm tra lại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    return render(request, 'store/login.html', {
        'frm_dang_ky': frm_dang_ky,
        'chuoi_kq_dang_ky': chuoi_kq_dang_ky,
        'chuoi_kq_dang_nhap': chuoi_kq_dang_nhap,
        'cart': cart,
    })


def customer_logout(request):
    if 's_khach_hang' in request.session:
        del request.session['s_khach_hang']
    return redirect('customer:login')


def my_account(request):
    # Giỏ hàng
    cart = Cart(request)

    chuoi_kq_change_pass = '';
    chuoi_kq_change_diachi = '';

    orders_status = ' show active ';
    address_status = '';
    pass_status = '';

    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_khach_hang' not in request.session:
        return redirect('customer:my-account/')

    # Cập nhật thông tin tài khoản
    if request.POST.get('btnCapNhat'):
        # Gán biến
        ho = request.POST.get('ho')
        ten = request.POST.get('ten')
        dien_thoai = request.POST.get('dien_thoai')
        dia_chi = request.POST.get('dia_chi')

        # Cập nhật
        s_khach_hang = request.session.get('s_khach_hang')
        khach_hang = KhachHang.objects.get(id=s_khach_hang['id'])
        khach_hang.ho = ho
        khach_hang.ten = ten
        khach_hang.dien_thoai = dien_thoai
        khach_hang.dia_chi = dia_chi
        khach_hang.save()

        # Cập nhật vào session hiện tại (s_khach_hang)
        s_khach_hang['ho'] = ho
        s_khach_hang['ten'] = ten
        s_khach_hang['dien_thoai'] = dien_thoai
        s_khach_hang['dia_chi'] = dia_chi

        orders_status = '';
        address_status = ' show active ';
        pass_status = '';

        chuoi_kq_change_diachi = '''
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        Cập nhật thành công.
                    </div>
                    '''

    # Đổi mật khẩu
    form = FormDoiMatKhau()
    
    if request.POST.get('btnChangePass'):
        form = FormDoiMatKhau(request.POST, KhachHang)
        
        print("Test123");
        orders_status = '';
        address_status = '';
        pass_status = ' show active ';

        if form.is_valid():

            mat_khau_hien_tai = form.cleaned_data['mat_khau_hien_tai']
            s_khach_hang = request.session.get('s_khach_hang')
            khach_hang = KhachHang.objects.get(id=s_khach_hang['id'])

            hasher = Argon2PasswordHasher()
            encoded = hasher.encode(mat_khau_hien_tai, '12345678')

            if encoded == khach_hang.mat_khau:
                if form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
                    
                    print('change pass')
                    khach_hang.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], '12345678')
                    khach_hang.save()

                    chuoi_kq_change_pass = '''
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        Cập nhật thành công.
                    </div>
                    '''
                else:
                    chuoi_kq_change_pass = '''
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Mật khẩu xác nhận không đúng. Vui lòng nhập lại!
                    </div>
                    '''
            else:

                chuoi_kq_change_pass = '''
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Mật khẩu không đúng. Vui lòng nhập lại!
                    </div>
                    '''
    
    return render(request, 'store/my-account.html', {
        'cart': cart,
        'form': form,
        'chuoi_kq_change_pass': chuoi_kq_change_pass,
        'chuoi_kq_change_diachi' : chuoi_kq_change_diachi,
        'address_status':address_status,
        'orders_status':orders_status,
        'pass_status':pass_status
    })


