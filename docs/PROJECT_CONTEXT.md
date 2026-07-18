# Billix — Project Context

> Single source of truth for every AI assistant (Bolt AI, Cursor, Claude,
> ChatGPT, Jules, Trae, etc.). Read this document before implementing anything.

## 1. Project Overview

**Billix** is a production-ready GST Billing, Inventory & Business Management
SaaS application. It is designed for small and medium businesses that need
end-to-end GST compliance, inventory tracking, customer/supplier management,
invoicing, payments, and reporting — all within a single multi-tenant platform.

This is **not** a demo, tutorial, or college project. Every line of code is
intended to run in production and serve real businesses. Treat the codebase
with the same rigor as any commercial SaaS product.

## 2. Purpose

Billix exists to simplify the operational backbone of a business:

- Accurate GST-compliant invoicing.
- Real-time inventory tracking.
- Unified customer and supplier ledger management.
- Payment tracking and reconciliation.
- Actionable reports and analytics.
- Multi-tenant isolation so each business's data stays private.

The product must remain reliable, secure, and auditable. A missed invoice or
corrupted inventory record has real-world financial consequences.

## 3. Features

### Core Modules

- **Identity & Authentication** — Clerk-based login, signup, session
  management, role assignment.
- **Multi-Tenant Business Foundation** — Each user belongs to one or more
  businesses; data is strictly isolated per tenant.
- **Customer Module** — Customer onboarding, contact management, ledger
  view, outstanding balances.
- **Supplier Module** — Supplier onboarding, purchase tracking, payable
  ledgers.
- **Product Module** — Product catalog, GST rates, HSN/SAC codes, pricing.
- **Inventory Module** — Stock levels, stock movements, low-stock alerts,
  warehouse tracking.
- **Invoice Module** — GST invoices, credit notes, estimates, e-invoice
  compliance, PDF generation.
- **Payments** — Payment recording, UPI/bank reconciliation, partial
  payments, payment links.
- **Reports & Analytics** — GST returns (GSTR-1, GSTR-3B), sales/purchase
  summaries, inventory valuation, dashboard KPIs.

### Cross-Cutting Capabilities

- Role-based access control (owner, admin, accountant, staff).
- Audit logs for sensitive operations.
- Error monitoring via Sentry.
- File storage (invoices, documents) via Appwrite.
- Responsive UI usable on desktop and tablet.

## 4. Tech Stack

### Frontend

| Concern        | Technology             |
| -------------- | ---------------------- |
| UI library     | React 19               |
| Language       | TypeScript             |
| Build tool     | Vite                   |
| Routing        | TanStack Router        |
| Data fetching  | TanStack Query         |
| Styling        | TailwindCSS            |
| Component lib  | shadcn/ui (new-york)   |
| Forms          | react-hook-form + zod  |
| Icons          | lucide-react           |
| Charts         | recharts               |
| Notifications  | sonner                 |

### Backend

| Concern        | Technology             |
| -------------- | ---------------------- |
| Framework      | FastAPI                |
| Language       | Python 3.13+           |
| ORM            | SQLAlchemy 2.0         |
| Migrations     | Alembic                |
| Database       | PostgreSQL (Neon)      |

### Platform Services

| Concern        | Service                |
| -------------- | ---------------------- |
| Authentication | Clerk                  |
| Storage        | Appwrite               |
| Monitoring     | Sentry                 |

### Deployment

| Layer           | Target       |
| --------------- | ------------ |
| Frontend        | Vercel       |
| Backend         | DigitalOcean |
| Database        | Neon         |

## 5. Deployment

- **Frontend** is deployed to Vercel and served via the global edge network.
  Builds are triggered from the connected branch.
- **Backend** is deployed to a DigitalOcean droplet (or app platform) running
  the FastAPI process behind a reverse proxy. Alembic migrations run as part
  of the release pipeline.
- **Database** is hosted on Neon with branching enabled for staging.
- **Environment variables** (Clerk keys, Appwrite endpoint, Sentry DSN,
  database URL) are injected at the platform level and never committed.

## 6. Current Project Status

### Completed

- Backend Foundation — FastAPI project scaffold, configuration, logging,
  dependency wiring.
- Database Infrastructure — Neon PostgreSQL provisioned, Alembic baseline,
  connection pooling.
- Clerk Configuration (`AUTH-001`) — Clerk application created, keys stored,
  frontend integration scaffolded.

### Current Milestone

**Milestone 3 — Identity & Authentication Foundation**

### Upcoming Engineering Tickets

| Ticket    | Title                          |
| --------- | ------------------------------ |
| `AUTH-002`| Backend Clerk Integration      |
| `AUTH-003`| User Model                     |
| `AUTH-004`| Authentication Middleware      |
| `AUTH-005`| Current User Dependency         |
| `AUTH-006`| Role Foundation                |
| `AUTH-007`| Protected Routes               |
| `AUTH-008`| Authentication Testing          |

See `docs/ROADMAP.md` for the full milestone breakdown and completion criteria.

## 7. Future Roadmap Summary

The roadmap is split into 12 milestones, each delivering a coherent slice of
business value:

1. Backend Foundation
2. Database Infrastructure
3. Identity & Authentication
4. Multi-Tenant Business Foundation
5. Customer Module
6. Supplier Module
7. Product Module
8. Inventory Module
9. Invoice Module
10. Payments
11. Reports & Analytics
12. Deployment

Each milestone is broken into engineering tickets with explicit completion
criteria. AI assistants must implement one ticket at a time and never jump
ahead to future milestones.

## 8. AI Instructions

Every AI assistant working on Billix must:

1. Read all four documentation files **before** writing or modifying any
   code:
   - `docs/PROJECT_CONTEXT.md`
   - `docs/ARCHITECTURE.md`
   - `docs/ROADMAP.md`
   - `docs/AI_RULES.md`
2. Treat these documents as the single source of truth. If something in the
   codebase contradicts the docs, flag it to the human owner — do not
   silently "fix" it.
3. Implement only the ticket explicitly requested. Never implement future
   milestones, speculative features, or unrelated refactors.
4. Follow the existing folder structure, naming conventions, and coding
   standards described in `docs/ARCHITECTURE.md`.
5. Stop after completing the requested ticket, summarize what changed, and
   wait for the next instruction.
