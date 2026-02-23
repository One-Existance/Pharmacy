from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import InventoryLog, Medicine, Prescription, Sale, SaleItem, Supplier, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	ordering = ("email",)
	list_display = ("email", "full_name", "role", "is_staff", "is_active")
	fieldsets = (
		(None, {"fields": ("email", "password")}),
		("Personal info", {"fields": ("full_name", "role")}),
		("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
		("Important dates", {"fields": ("last_login", "created_at")}),
	)
	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("email", "full_name", "role", "password1", "password2", "is_staff", "is_superuser"),
			},
		),
	)
	search_fields = ("email", "full_name")
	readonly_fields = ("created_at",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
	list_display = ("supplier_name", "phone")
	search_fields = ("supplier_name", "phone")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
	list_display = ("medicine_name", "category", "price", "quantity", "expiry_date", "supplier")
	search_fields = ("medicine_name", "category")
	list_filter = ("category", "expiry_date")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
	list_display = ("sale_id", "sale_date", "total_amount", "user")
	list_filter = ("sale_date",)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
	list_display = ("sale", "medicine", "quantity", "price")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
	list_display = ("prescription_id", "customer_name", "doctor_name", "prescription_date")
	search_fields = ("customer_name", "doctor_name")


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
	list_display = ("inventory_id", "medicine", "change_type", "quantity_changed", "log_date")
	list_filter = ("change_type", "log_date")
