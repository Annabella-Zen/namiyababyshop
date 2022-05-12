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




     # Đổi mật khẩu
    frm_doi_mat_khau = FormDoiMatKhau()
    chuoi_kq_doi_mat_khau = ''
    if request.POST.get('btnChangePass'):
        frm_doi_mat_khau = FormDoiMatKhau(request.POST, KhachHang)
        
        # Gán biến
        mat_khau = request.POST.get('mat_khau_hien_tai')

        # Check mật khẩu == xác nhận mật khẩu
        if frm_doi_mat_khau.is_valid() and frm_doi_mat_khau.cleaned_data['mat_khau'] == frm_doi_mat_khau.cleaned_data['xac_nhan_mat_khau']:
            

            hasher = Argon2PasswordHasher() 
            request.POST.__mutable = True

            s_khach_hang = request.session.get('s_khach_hang')
            khach_hang = KhachHang.objects.get(id=s_khach_hang['id'])
            khach_hang.mat_khau_hien_tai = frm_doi_mat_khau.cleaned_data['mat_khau']
            khach_hang.mat_khau = frm_doi_mat_khau.cleaned_data['mat_khau']
            
            if KhachHang.objects.filter(mat_khau=khach_hang.mat_khau_hien_tai):
                # return render(request, 'store/login_error.html')
                chuoi_kq_doi_mat_khau = 'Thay đổi mật khẩu không thành công'
            else:
                khach_hang.mat_khau = hasher.encode(frm_doi_mat_khau.cleaned_data['mat_khau'], '12345678')

                khach_hang.save()
                
                # Cập nhật vào session hiện tại
                s_khach_hang['mat_khau'] = mat_khau
                chuoi_kq_doi_mat_khau = 'Thay đổi mật khẩu thành công'

    return render(request, 'store/my-account.html', {
        'frm_doi_mat_khau': frm_doi_mat_khau,
        'chuoi_kq_doi_mat_khau': chuoi_kq_doi_mat_khau,
        'cart': cart
    })


