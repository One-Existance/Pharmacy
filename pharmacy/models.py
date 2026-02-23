import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError("The Email field is required")

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("role", User.Role.ADMIN)
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True")

		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	class Role(models.TextChoices):
		ADMIN = "admin", "Admin"
		PHARMACIST = "pharmacist", "Pharmacist"
		CASHIER = "cashier", "Cashier"

	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	full_name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	role = models.CharField(max_length=50, choices=Role.choices)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["full_name"]

	def __str__(self):
		return f"{self.full_name} ({self.email})"


class Supplier(models.Model):
	supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	supplier_name = models.CharField(max_length=255)
	phone = models.CharField(max_length=20)
	address = models.CharField(max_length=500)

	def __str__(self):
		return self.supplier_name


class Medicine(models.Model):
	medicine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	medicine_name = models.CharField(max_length=255)
	category = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.IntegerField()
	expiry_date = models.DateField(null=True, blank=True)
	supplier = models.ForeignKey(
		Supplier,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="medicines",
	)

	def __str__(self):
		return self.medicine_name


class Sale(models.Model):
	sale_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sale_date = models.DateTimeField(auto_now_add=True)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sales")

	def __str__(self):
		return f"Sale {self.sale_id}"


class SaleItem(models.Model):
	sale_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_items")
	medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name="sale_items")
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.medicine.medicine_name} x {self.quantity}"


class Prescription(models.Model):
	prescription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	customer_name = models.CharField(max_length=255)
	doctor_name = models.CharField(max_length=255)
	prescription_date = models.DateField()

	def __str__(self):
		return f"Prescription {self.prescription_id}"


class InventoryLog(models.Model):
	class ChangeType(models.TextChoices):
		ADD = "add", "Add"
		REMOVE = "remove", "Remove"
		ADJUST = "adjust", "Adjust"

	inventory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="inventory_logs")
	change_type = models.CharField(max_length=50, choices=ChangeType.choices)
	quantity_changed = models.IntegerField()
	log_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.medicine.medicine_name} - {self.change_type}"
