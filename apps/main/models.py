from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from decimal import Decimal

class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)

    class Meta:
        ordering = ['title']
        indexes = [models.Index(fields=["title"])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug=f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    image = models.ImageField(upload_to="product/main", blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True, verbose_name="В наличии")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00,)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def sell_price(self):
        if self.discount:
           return round(self.price - self.price / 100, 2)
        return self.price
    
    # возращает скидку 
    def get_discount_percent(self):
        return round(self.discount, 0)
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/gallery", blank=True, null=True, verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Фотография товара'
        verbose_name_plural ='Фотографии товара'
    
    def __str__(self):
        return f"Изображение товара: {self.product.title}"