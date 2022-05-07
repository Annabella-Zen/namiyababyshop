from django.contrib import admin

# Register your models here.
from django.contrib import admin
from store.models import *
from datetime import datetime
from django.utils.html import format_html


# Register your models here.
def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())

change_public_day.short_description = 'Change public_day to Today'


class ProductAdmin(admin.ModelAdmin):
    # Không hiển thị trên trang thêm/cập nhật
    exclude = ('public_day', 'viewed')

    # Hiển thị trên danh sách
    # list_display = ('name', 'price', 'public_day', 'viewed')
    list_display = ('e_name', 'e_price', 'e_public_day', 'e_viewed', 'e_image')

    # Lọc
    list_filter = ('public_day',)

    # Tìm kiếm
    search_fields = ('name__contains',)

    # Action
    actions = [change_public_day]

    @admin.display(description="Tên sản phẩm")
    def e_name(self, obj):
        return '%s' % obj.name

    @admin.display(description="Giá")
    def e_price(self, obj):
        return '%s' % "{:,}".format(int(obj.price)) 

    @admin.display(description="Ngày xuất bản")
    def e_public_day(self, obj):
        return '%s' % obj.public_day

    @admin.display(description="Số lượt xem")
    def e_viewed(self, obj):
        return '%s' % obj.viewed

    @admin.display(description="Hình ảnh")
    def e_image(self, obj):
        return format_html('<img src="%s" alt="%s" style="width: 45px; height: 45px;" />' % (obj.image.url, obj.name))



admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubCategoryLevel2)
admin.site.register(Product, ProductAdmin)


# Thay đổi tiêu đề trang admin (góc trên bên trái và tiêu đề form login)
admin.site.site_header = 'BabyStore Admin'




