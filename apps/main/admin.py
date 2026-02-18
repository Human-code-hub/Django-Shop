from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse


admin.site.site_header = "Glyse shop"
admin.site.site_title = "My shop"
admin.site.index_title = "Welcome to the administrator"

@admin.action(description="Сделать доступным")
def make_available(modeladmin, request, queryset):
    queryset.update(available=True)

@admin.action(description="Сделать товар не доступным")
def make_unavailable(modeladmin, request, queryset):
    queryset.update(available=False)

@admin.action(description="Убрать скидку")
def reset_discount(modeladmin, request, queryset):
    queryset.update(discount=0)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    ordering = ("order",)
    fields =[
        'preview',
        'image',
        'order',
    ]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj and obj.image:
            return format_html (
                '<img class="inline-preview-img" src="{}" width="70" style="border-radius:6px;">',
                obj.image.url
            )
        return format_html (
            '<img class="inline-preview-img" width="80" style="display:none; border-radius:6px;"><br>'
            '<span class="no-photo-text" style="color:#888; font-style:italic;">нету фото</span>'
        )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title', 'slug']
    prepopulated_fields = {"slug": ("title", )}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = ("admin/js/image_preview.js",)

    list_display = ["image_tag", "title", "slug", "category", "price", "discount", "final_price", "available", "delete_link", 'created_at', 'updated_at']
    list_filter = ["title","available","category"]
    list_editable = ["price", "discount", "available"]
    actions = [make_available, make_unavailable, reset_discount]
    search_fields = ["title", "slug", "category__title"]
    inlines = [ProductImageInline]
    fieldsets = [
        ("Основные",{'fields': ["title", "slug", "category", "description"]}),
        ("Изображения",{'fields': ["image", "main_image_preview"]}),
        ("Цена",{'fields': ["price", 'discount']}),
        ("Статус",{'fields': ["available"]}),
        ("Системные",{'fields': ["created_at", "updated_at"], "classes":("collapse",)}),
    ]
    readonly_fields = [
        "main_image_preview",
        "created_at",
        'updated_at',
    ]
    prepopulated_fields = {"slug": ("title",)}

    def main_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
            '<img id="main-image-preview" src="{}" '
            'style="width:120px; height:150px; '
            'object-fit:cover; '
            'border-radius:8px; '
            'box-shadow:0 4px 10px rgba(0,0,0,0.25); '
            'transition: opacity 0.3s ease; '
            'opacity:1;">',
            obj.image.url,
            )

        return format_html(
            '<div class="main-image-container">'
            '<img id="main-image-preview" '
            'style="display:none; width:120px; height:150px; '
            'object-fit:cover; '
            'border-radius:8px; '
            'box-shadow:0 4px 10px rgba(0,0,0,0.25); '
            'transition: opacity 0.3s ease; '
            'opacity:0;">'
            '<br><span class="no-photo-text" '
            'style="color:#888; font-style:italic;">Нет фото</span>'
            '</div>'
            )

    def image_tag(self, obj):
        if obj.image:
            url = reverse("admin:main_product_change", args=[obj.pk])
            return format_html(
                '<a href="{}" >'
                '<img src="{}" width="50" height="60" style="border-radius:6px;"/>'
                '</a>',
                url,
                obj.image.url
            )
        return "-"
    
    image_tag.short_description = "Image"
    image_tag.admin_order_field = "Image"

    def delete_link(self, obj):
        if obj.pk:
            url = reverse("admin:main_product_delete", args=[obj.pk])
            return format_html(
                '<a href="{}" >Удалить</a>', url
            )
        return "-"
    
    delete_link.short_description = "Удалить"

    def final_price(self, obj):
        final_price = obj.sell_price
        if obj.discount > 0:
            return format_html (
                '<span style="color:#d9534f; font-weight:600;"> {} грн</span>', final_price
            )
        else:
            return format_html (
                '<span style="color:#5cb85c; font-weight:600"> {} грн</span>', obj.price
            )
    
    final_price.short_description = "Final_price"
    final_price.admin_order_field = "price"