# EM Test Case

Custom authentication and authorization backend system.

## Stack

- Python 3.14, Django, DRF, PostgreSQL, drf-spectacular, loguru, bcrypt
- Token-based auth (SHA-512), hybrid RBAC+ABAC

## Quick Start

```bash
make up        # Build and start services
make down      # Down services
make migrate   # Apply migrations
make test      # Run tests with coverage
make lint      # Run ruff linter
```

OpenAPI docs available at `http://0.0.0.0:8000/api/docs`.

## Project Structure

```
src/
├── config/          # Django settings, ASGI, WSGI, URLs
├── core/            # Base models, domain enums, exceptions
├── authentication/  # Token auth backend & middleware
├── access_control/  # RBAC+ABAC models & logic
└── business/        # Business logic layer
```

## Access Control Model

### Roles

| Role    | Description |
|---------|-------------|
| admin   | Full access to all resources |
| manager | Can manage orders and products |
| user    | Can read products, create orders |

### Business Elements

| Element    | Description |
|------------|-------------|
| products   | Product catalog |
| orders     | Customer orders |
| reports    | Business reports |
| customers  | Customer data |

### Permission Model

Each role-element pair defines an `AccessRule` with the following permissions:

| Permission       | Description |
|------------------|-------------|
| `can_read`       | Can read own records |
| `can_read_all`   | Can read all records |
| `can_create`     | Can create records |
| `can_update`     | Can update own records |
| `can_update_all` | Can update all records |
| `can_delete`     | Can delete own records |
| `can_delete_all` | Can delete all records |

## Seed Data

- **3 roles**: admin, manager, user
- **4 business elements**: products, orders, reports, customers
- **12 access rules** covering all role-element combinations
- **3 users**: admin@example.com, manager@example.com, user@example.com (passwords: `admin123`, `manager123`, `user123`)