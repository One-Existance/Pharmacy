from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    InventoryLogViewSet,
    MedicineViewSet,
    PrescriptionViewSet,
    SaleViewSet,
    SupplierViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("suppliers", SupplierViewSet, basename="supplier")
router.register("medicines", MedicineViewSet, basename="medicine")
router.register("sales", SaleViewSet, basename="sale")
router.register("prescriptions", PrescriptionViewSet, basename="prescription")
router.register("inventory-logs", InventoryLogViewSet, basename="inventory-log")

urlpatterns = [
    path("", include(router.urls)),
]