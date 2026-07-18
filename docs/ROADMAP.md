# Billix — Roadmap

> Read alongside `docs/PROJECT_CONTEXT.md` and `docs/ARCHITECTURE.md`.
> AI assistants implement one ticket at a time, in order, and never jump
> ahead to future milestones.

## Milestone 1 — Backend Foundation

**Objective:** Establish a production-grade FastAPI backend with
configuration, logging, error handling, and a runnable application
factory.

**Engineering Tickets:**

- `BE-001` — FastAPI project scaffold and folder structure
- `BE-002` — pydantic-settings configuration loader
- `BE-003` — Structured logging and request-id middleware
- `BE-004` — Global error handler and Sentry integration
- `BE-005` — Health-check and readiness endpoints
- `BE-006` — Linting (Ruff/Black) and CI pipeline

**Completion Criteria:**

- `uvicorn app.main:app` boots cleanly.
- `/healthz` returns 200; `/readyz` checks DB connectivity.
- Unhandled exceptions are reported to Sentry and return a consistent error
  envelope.
- CI runs lint + tests on every PR.

## Milestone 2 — Database Infrastructure

**Objective:** Provision PostgreSQL on Neon, wire SQLAlchemy 2.0 and
Alembic, and establish the migration workflow.

**Engineering Tickets:**

- `DB-001` — Neon project provisioning and connection string
- `DB-002` — SQLAlchemy 2.0 declarative base and engine
- `DB-003` — Session dependency and scoped session lifecycle
- `DB-004` — Alembic baseline and env wiring
- `DB-005` — Migration authoring guide and CI check
- `DB-006` — Connection pooling and timeout tuning

**Completion Criteria:**

- Alembic can upgrade/downgrade against a fresh database.
- `get_session` dependency yields a session per request.
- A baseline migration exists and is reversible.
- CI rejects PRs that introduce migration drift.

## Milestone 3 — Identity & Authentication

**Objective:** Establish Clerk-based authentication end-to-end, the User
model, role foundation, and protected routes.

**Engineering Tickets:**

- `AUTH-001` — Clerk application configuration (completed)
- `AUTH-002` — Backend Clerk integration (JWT verification, JWKS)
- `AUTH-003` — User model (mirrors Clerk users)
- `AUTH-004` — Authentication middleware
- `AUTH-005` — Current user dependency
- `AUTH-006` — Role foundation (role enum + permissions matrix)
- `AUTH-007` — Protected routes and route guards
- `AUTH-008` — Authentication testing (unit + integration)

**Completion Criteria:**

- A signed Clerk JWT is verified on every protected route.
- Unauthenticated requests receive 401; unauthorized roles receive 403.
- `current_user` is injectable into any route handler.
- Tests cover happy path, expired tokens, and wrong-tenant scenarios.

## Milestone 4 — Multi-Tenant Business Foundation

**Objective:** Allow a user to create/join businesses, switch active
tenants, and enforce strict tenant isolation across all data.

**Engineering Tickets:**

- `TEN-001` — Business (tenant) model
- `TEN-002` — Business memberships model and roles
- `TEN-003` — Tenant resolution middleware (active tenant header)
- `TEN-004` — Tenant-scoped repository base
- `TEN-005` — Business CRUD API
- `TEN-006` — Membership invite/accept flow
- `TEN-007` — Tenant isolation tests

**Completion Criteria:**

- A user can create a business and invite members.
- All tenant-scoped queries filter by `tenant_id` automatically.
- Cross-tenant access returns 403 and is covered by tests.

## Milestone 5 — Customer Module

**Objective:** Manage customers with GST details, contact info, and
ledger summaries.

**Engineering Tickets:**

- `CUST-001` — Customer model and migration
- `CUST-002` — Customer schemas
- `CUST-003` — Customer repository
- `CUST-004` — Customer service (dedupe, GST validation)
- `CUST-005` — Customer API (CRUD + search)
- `CUST-006` — Customer UI (list, detail, create/edit)
- `CUST-007` — Outstanding balance aggregation

**Completion Criteria:**

- Customers are tenant-scoped and searchable by name/GSTIN/phone.
- Duplicate GSTIN detection works within a tenant.
- Ledger view shows receivables per customer.

## Milestone 6 — Supplier Module

**Objective:** Manage suppliers with GST details and payable ledgers.

**Engineering Tickets:**

- `SUP-001` — Supplier model and migration
- `SUP-002` — Supplier schemas
- `SUP-003` — Supplier repository
- `SUP-004` — Supplier service
- `SUP-005` — Supplier API
- `SUP-006` — Supplier UI
- `SUP-007` — Payable balance aggregation

**Completion Criteria:**

- Suppliers are tenant-scoped and searchable.
- Payable ledger reflects unpaid purchase invoices.

## Milestone 7 — Product Module

**Objective:** Maintain a product catalog with GST rates, HSN/SAC codes,
and pricing.

**Engineering Tickets:**

- `PROD-001` — Product model and migration
- `PROD-002` — Tax rate / HSN reference data
- `PROD-003` — Product schemas
- `PROD-004` — Product repository
- `PROD-005` — Product service (pricing, tax mapping)
- `PROD-006` — Product API
- `PROD-007` — Product UI

**Completion Criteria:**

- Products support multiple tax slabs and units of measurement.
- HSN/SAC codes are validated against reference data.

## Milestone 8 — Inventory Module

**Objective:** Track stock levels, movements, and low-stock alerts across
warehouses.

**Engineering Tickets:**

- `INV-001` — Warehouse model
- `INV-002` — Stock item model and migration
- `INV-003` — Stock movement model (immutable ledger)
- `INV-004` — Inventory repository
- `INV-005` — Inventory service (atomic stock adjustments)
- `INV-006` — Low-stock alert rules
- `INV-007` — Inventory API
- `INV-008` — Inventory UI

**Completion Criteria:**

- Stock movements are append-only and auditable.
- Concurrent adjustments do not produce negative stock.
- Low-stock alerts trigger on configurable thresholds.

## Milestone 9 — Invoice Module

**Objective:** Generate GST-compliant invoices, credit notes, and
estimates with PDF output.

**Engineering Tickets:**

- `INVC-001` — Invoice model and migration (header + line items)
- `INVC-002` — Invoice numbering scheme (tenant-scoped sequence)
- `INVC-003` — GST calculation service (CGST/SGST/IGST)
- `INVC-004` — Invoice repository
- `INVC-005` — Invoice service (create, amend, cancel, credit note)
- `INVC-006` — e-Invoice integration (IRN generation)
- `INVC-007` — PDF generation and Appwrite storage
- `INVC-008` — Invoice API
- `INVC-009` — Invoice UI

**Completion Criteria:**

- Invoices compute GST correctly for intra- and inter-state supplies.
- Invoice numbers are unique and gapless per tenant per financial year.
- PDFs are stored in Appwrite and downloadable via signed URLs.

## Milestone 10 — Payments

**Objective:** Record payments, reconcile against invoices, and expose
payment links.

**Engineering Tickets:**

- `PAY-001` — Payment model and migration
- `PAY-002` — Payment repository
- `PAY-003` — Payment service (allocation, partial payments)
- `PAY-004` — Reconciliation rules engine
- `PAY-005` — Payment gateway integration (UPI/bank)
- `PAY-006` — Payment link generation
- `PAY-007` — Payment API
- `PAY-008` — Payment UI

**Completion Criteria:**

- Payments can be allocated across multiple invoices.
- Overpayments are tracked as credit on the customer account.
- Payment links expire and are idempotent.

## Milestone 11 — Reports & Analytics

**Objective:** Provide GST returns, sales/purchase summaries, inventory
valuation, and a dashboard.

**Engineering Tickets:**

- `RPT-001` — Reporting read models / materialized views
- `RPT-002` — GSTR-1 report
- `RPT-003` — GSTR-3B report
- `RPT-004` — Sales summary report
- `RPT-005` — Purchase summary report
- `RPT-006` — Inventory valuation report
- `RPT-007` — Dashboard KPIs service
- `RPT-008` — Reports API
- `RPT-009` — Reports UI (charts, filters, export)

**Completion Criteria:**

- GSTR-1 and GSTR-3B outputs match the GSTN prescribed format.
- Reports support date-range, tenant, and customer/supplier filters.
- Dashboard KPIs load in under 500ms p95.

## Milestone 12 — Deployment

**Objective:** Ship Billix to production with CI/CD, observability, and
runbooks.

**Engineering Tickets:**

- `DEP-001` — Vercel frontend pipeline
- `DEP-002` — DigitalOcean backend pipeline
- `DEP-003` — Alembic migration runner in release
- `DEP-004` — Sentry release tracking and source maps
- `DEP-005` — Staging environment on Neon branch
- `DEP-006` — Secrets management and rotation runbook
- `DEP-007` — Uptime and synthetic monitoring
- `DEP-008` — Incident response runbook

**Completion Criteria:**

- Merging to `main` deploys to staging; manual promotion to production.
- Migrations run automatically and fail the deploy on error.
- Sentry captures frontend and backend errors with release tags.
- Runbooks exist for rollback, secret rotation, and tenant data export.
