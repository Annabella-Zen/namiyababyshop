from tkinter import CURRENT
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')

    def __str__(self):
        return self.name


class SubCategoryLevel2(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    subcategorylevel2 = models.ForeignKey(SubCategoryLevel2, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')
    content = RichTextField(blank=True, null=True)
    public_day = models.DateTimeField(auto_now=False, auto_now_add=True, null = True)
    evaluate = models.TextField(default="100%")
    information = RichTextUploadingField(blank=True, null=True)
    detail_information = RichTextUploadingField(blank=True, null=True)
    policies = RichTextUploadingField(blank=True, null=True)
    comment = RichTextUploadingField(blank=True, null=True)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-public_day']





class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    portfolio = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', default="users/no_avatar.png")

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = u'userprofileinfo'