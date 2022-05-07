from django.db import models


# Create your models here.
class KhachHang(models.Model):
    ho = models.CharField(max_length=264, blank=True)
    ten = models.CharField(max_length=264, blank=True)
    email = models.EmailField(blank=False)
    mat_khau = models.CharField(max_length=50, blank=False)
    dien_thoai = models.CharField(max_length=20, blank=True)
    dia_chi = models.TextField(blank=True)

    def __str__(self):
        return self.email
