# Pharmacy Management System (Django)

This project implements the pharmacy system from the SRS document and ERD.

## Implemented Modules

- User management with roles (`admin`, `pharmacist`, `cashier`)
- Supplier management
- Medicine inventory management
- Sales and sale items
- Prescription records
- Inventory logs
- Django admin for all models
- REST API endpoints under `/api/`

## Tech Stack

- Django
- Django REST Framework
- SQLite (default)

## Setup

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

- `/api/users/`
- `/api/suppliers/`
- `/api/medicines/`
- `/api/sales/`
- `/api/prescriptions/`
- `/api/inventory-logs/`

## Notes

- Sales creation supports nested `sale_items` and automatically:
  - Deducts medicine stock quantity
  - Creates inventory log entries (`remove`)
  - Calculates and stores `total_amount`
