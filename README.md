# EM Test Case

Custom authentication and authorization backend system.

## Stack

- Python 3.14, Django 6.0.6, DRF 3.17.1
- PostgreSQL 17, psycopg 3
- Token-based auth (SHA-256), hybrid RBAC+ABAC
- drf-spectacular (OpenAPI), loguru, bcrypt

## Quick Start

```bash
make up        # Build and start services
make migrate   # Apply migrations
make test      # Run tests with coverage
make lint      # Run ruff linter
```

## Project Structure

```
src/
├── config/          # Django settings, ASGI, WSGI, URLs
├── core/            # Base models, domain enums, exceptions
├── authentication/  # Token auth backend & middleware
├── access_control/  # RBAC+ABAC models & logic
└── business/        # Business logic layer