from rest_framework import filters, permissions, viewsets

from .models import InventoryLog, Medicine, Prescription, Sale, Supplier, User
from .permissions import IsAdminOrReadOnly, IsAdminRole
from .serializers import (
    InventoryLogSerializer,
    MedicineSerializer,
    PrescriptionSerializer,
    SaleSerializer,
    SupplierSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ["full_name", "email", "role"]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("supplier_name")
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["supplier_name", "phone", "address"]


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.select_related("supplier").all().order_by("medicine_name")
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["medicine_name", "category"]


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related("user").prefetch_related("sale_items").all().order_by("-sale_date")
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by("-prescription_date")
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["customer_name", "doctor_name"]


class InventoryLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryLog.objects.select_related("medicine").all().order_by("-log_date")
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
