from django import forms
from customer.models import KhachHang

class FormDangNhap:
    email = forms.CharField(max_length=100)
    mat_khau = forms.CharField(max_length=20)


class FormDangKy(forms.ModelForm):

    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email",
    }))
    mat_khau = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu",
    }))
    xac_nhan_mat_khau = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Xác nhận mật khẩu",
    }))


    class Meta:
        model = KhachHang
        fields = [ 'email', 'mat_khau']


class FormDoiMatKhau(forms.ModelForm):
    mat_khau_hien_tai = forms.CharField(label='Mật khẩu hiện tại', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu hiện tại",
    }))
    mat_khau = forms.CharField(label='Mật khẩu mới', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu mới",
    }))
    xac_nhan_mat_khau = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Xác nhận Mật khẩu",
    }))

    class Meta:
        model = KhachHang
        fields = ['mat_khau_hien_tai', 'mat_khau', 'xac_nhan_mat_khau']
