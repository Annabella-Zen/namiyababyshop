# Register your models here.
from django.contrib import admin
from customer.models import *
from datetime import datetime
from django.utils.html import format_html


# Register your models here.
def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())

change_public_day.short_description = 'Change public_day to Today'


class CustomerAdmin(admin.ModelAdmin):

    # Hiển thị trên danh sách
    list_display = ('e_ho', 'e_ten', 'e_email', 'e_dien_thoai', 'e_dia_chi')

    # Lọc
    list_filter = ('dia_chi',)

    # Tìm kiếm
    search_fields = ('email__contains',)

    # Action

    @admin.display(description="Họ")
    def e_ho(self, obj):
        return '%s' % obj.ho

    @admin.display(description="Tên")
    def e_ten(self, obj):
        return '%s' % obj.ten

    @admin.display(description="Email")
    def e_email(self, obj):
        return '%s' % obj.email

    @admin.display(description="Điện thoại")
    def e_dien_thoai(self, obj):
        return '%s' % obj.dien_thoai

    @admin.display(description="Địa chỉ")
    def e_dia_chi(self, obj):
        return '%s' % obj.dia_chi



admin.site.register(KhachHang, CustomerAdmin)


# Thay đổi tiêu đề trang admin (góc trên bên trái và tiêu đề form login)
admin.site.site_header = 'BabyStore Admin'




