from django.db import models
from django.urls import reverse

# Create your models here.

class MainCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/main_category_img', blank=True)

    class Meta:
        verbose_name = 'main category'
        verbose_name_plural = 'main categories'

    def __str__(self):
        return self.category_name

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory,on_delete=models.CASCADE,null=True,blank=True)
    category_name = models.CharField(max_length = 50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/category_img',blank=True)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('store_app:products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
