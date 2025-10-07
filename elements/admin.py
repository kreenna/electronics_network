from django.contrib import admin
from django.utils.html import format_html

from elements.models import Product, Factory, RetailNetwork, IndividualEntrepreneur


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "description")
    search_fields = ("id", "user")


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "supplier_link", "debt_to_supplier", "created_at")
    list_filter = ("city",)
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/elements/factory/{obj.supplier.id}/change/"
            return format_html("<a href='{}'>{}</a>", url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена у {updated} объектов.")

    clear_debt.short_description = "Очистить задолженность"


@admin.register(RetailNetwork)
class RetailNetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "supplier_link", "debt_to_supplier", "created_at")
    list_filter = ("city",)
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier_factory:
            url = f"/admin/elements/factory/{obj.supplier_factory.id}/change/"
            return format_html("<a href='{}'>{}</a>", url, obj.supplier_factory.name)
        if obj.supplier_network:
            url = f"/admin/elements/retailnetwork/{obj.supplier_network.id}/change/"
            return format_html("<a href='{}'>{}</a>", url, obj.supplier_network.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена у {updated} объектов.")

    clear_debt.short_description = "Очистить задолженность"


@admin.register(IndividualEntrepreneur)
class IndividualEntrepreneurAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "supplier_link", "debt_to_supplier", "created_at")
    list_filter = ("city",)
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier_factory:
            url = f"/admin/elements/factory/{obj.supplier_factory.id}/change/"
            return format_html("<a href='{}'>{}</a>", url, obj.supplier_factory.name)
        if obj.supplier_retail:
            url = f"/admin/elements/retailnetwork/{obj.supplier_retail.id}/change/"
            return format_html("<a href='{}'>{}</a>", url, obj.supplier_retail.name)
        if obj.supplier_ie:
            url = f"/admin/elements/individualentrepreneur/{obj.supplier_ie.id}/change/"
            return format_html("<a href='{}'>{}</a>", url, obj.supplier_ie.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена у {updated} объектов.")

    clear_debt.short_description = "Очистить задолженность"
