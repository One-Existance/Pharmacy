from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import InventoryLog, Medicine, Prescription, Sale, SaleItem, Supplier, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["user_id", "full_name", "email", "password", "role", "created_at"]
        read_only_fields = ["user_id", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["sale_item_id", "sale", "medicine", "quantity", "price"]
        read_only_fields = ["sale_item_id", "sale", "price"]


class SaleSerializer(serializers.ModelSerializer):
    sale_items = SaleItemSerializer(many=True, write_only=True)
    items = SaleItemSerializer(many=True, source="sale_items", read_only=True)

    class Meta:
        model = Sale
        fields = ["sale_id", "sale_date", "total_amount", "user", "sale_items", "items"]
        read_only_fields = ["sale_id", "sale_date", "total_amount", "items"]

    @transaction.atomic
    def create(self, validated_data):
        sale_items_data = validated_data.pop("sale_items")
        sale = Sale.objects.create(**validated_data)

        total_amount = Decimal("0.00")
        for item_data in sale_items_data:
            medicine = item_data["medicine"]
            quantity = item_data["quantity"]

            if quantity <= 0:
                raise serializers.ValidationError("Sale item quantity must be greater than zero")
            if medicine.quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {medicine.medicine_name}. Available: {medicine.quantity}"
                )

            unit_price = medicine.price
            SaleItem.objects.create(sale=sale, medicine=medicine, quantity=quantity, price=unit_price)

            medicine.quantity -= quantity
            medicine.save(update_fields=["quantity"])

            InventoryLog.objects.create(
                medicine=medicine,
                change_type=InventoryLog.ChangeType.REMOVE,
                quantity_changed=quantity,
            )

            total_amount += unit_price * quantity

        sale.total_amount = total_amount
        sale.save(update_fields=["total_amount"])
        return sale


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = "__all__"