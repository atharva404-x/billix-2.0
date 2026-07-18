# Billix — Architecture

> Read alongside `docs/PROJECT_CONTEXT.md`. This document defines the
> structural rules every AI assistant must follow.

## 1. Folder Structure

Billix is a two-repo product (frontend and backend). The structure below is
the canonical layout. AI assistants must place new files inside the
matching location — never invent a parallel hierarchy.

### Frontend

```
frontend/
├─ public/
├─ src/
│  ├─ assets/
│  ├─ components/
│  │  ├─ ui/              # shadcn/ui primitives — do not hand-edit
│  │  └─ <module>/        # module-scoped composite components
│  ├─ features/           # one folder per business module
│  │  └─ <module>/
│  │     ├─ api/          # TanStack Query hooks + fetchers
│  │     ├─ components/
│  │     ├─ hooks/
│  │     ├─ routes/
│  │     └─ types.ts
│  ├─ hooks/              # global, cross-cutting hooks
│  ├─ lib/                # utilities, api client, helpers
│  │  ├─ api.ts           # base fetch wrapper, auth header injection
│  │  ├─ clerk.ts         # Clerk client wiring
│  │  └─ utils.ts         # cn() and small helpers
│  ├─ routes/             # TanStack Router route tree
│  ├─ server/             # TanStack Start server entry / SSR helpers
│  ├─ styles.css          # Tailwind entrypoint + design tokens
│  └─ types/              # global TypeScript types
├─ tests/
├─ vite.config.ts
└─ tsconfig.json
```

### Backend

```
backend/
├─ app/
│  ├─ api/
│  │  └─ v1/
│  │     ├─ routes/       # FastAPI routers (one file per resource)
│  │     └─ dependencies.py
│  ├─ core/
│  │  ├─ config.py        # pydantic-settings, env loading
│  │  ├─ security.py
│  │  ├─ logging.py
│  │  └─ sentry.py
│  ├─ db/
│  │  ├─ base.py          # declarative Base, engine, SessionLocal
│  │  └─ session.py       # get_session dependency
│  ├─ models/             # SQLAlchemy ORM models (one file per aggregate)
│  ├─ schemas/             # Pydantic v2 request/response schemas
│  ├─ services/           # business logic — no HTTP, no ORM definitions
│  ├─ repositories/       # data access layer (queries, CRUD)
│  ├─ middleware/         # auth, tenant, request-id, error handlers
│  ├─ utils/
│  └─ main.py             # FastAPI app factory
├─ alembic/
│  ├─ versions/
│  └─ env.py
├─ tests/
│  ├─ unit/
│  └─ integration/
├─ pyproject.toml
└─ .env.example
```

## 2. Backend Architecture

### Layering

The backend follows a strict four-layer model. Each layer may only call the
layer directly beneath it.

```
Routes (api/v1/routes) → Services → Repositories → Models / DB
   ↑ Pydantic schemas         ↑ business rules   ↑ SQL/ORM
```

- **Routes** — HTTP concerns only. Parse request, call a service, return a
  response. No business logic, no direct DB access.
- **Services** — Orchestrate business rules. Authoritative owners of
  cross-model invariants and transactions.
- **Repositories** — Own all SQLAlchemy queries. Routes and services must
  never issue raw queries.
- **Models** — SQLAlchemy ORM definitions. No behavior beyond simple
  defaults and column constraints.

### Application Factory

`app/main.py` exposes `create_app()` which:

1. Loads settings via `app/core/config.py`.
2. Initializes Sentry.
3. Registers middleware (request-id, error handler, auth, tenant).
4. Mounts routers under `/api/v1`.
5. Wires the Alembic-verified engine into `app/db/base.py`.

### Configuration

All configuration flows through `pydantic-settings`. Secrets are read from
environment variables; no secret is ever committed. A `.env.example` file
documents the required keys.

### Error Handling

- Unhandled exceptions are captured by the error-handler middleware and
  forwarded to Sentry.
- API errors return a consistent `{"error": {"code", "message", "details"}}`
  shape.
- HTTP status codes follow REST conventions (409 for conflicts, 422 for
  validation, 403 for tenant violations, etc.).

## 3. Frontend Architecture

### Routing

TanStack Router with a generated route tree under `src/routes/`. Routes are
file-based and code-split per route. Protected routes use a route guard that
checks Clerk auth state and redirects to `/sign-in` when unauthenticated.

### Data Fetching

All server state flows through TanStack Query. Each feature exposes its own
hooks in `features/<module>/api/`. The base fetch wrapper in `lib/api.ts`
injects the Clerk session token and the active tenant header.

### State Management

- **Server state** → TanStack Query.
- **Local UI state** → React `useState` / `useReducer`.
- **URL state** → TanStack Router search params.
- **Global client state** → kept minimal; prefer deriving from server state.

No Redux, Zustand, or similar global store unless explicitly approved.

### Component Conventions

- shadcn/ui primitives live in `src/components/ui/` and are managed by the
  CLI. Do not hand-edit them.
- Composite components live in `features/<module>/components/` and compose
  the primitives.
- Forms use `react-hook-form` + `zod` for validation; schemas are colocated
  with the feature.

## 4. Database Architecture

### Engine

- PostgreSQL on Neon.
- SQLAlchemy 2.0 with the async-capable declarative base.
- Connection pooling via SQLAlchemy's pool; Neon's pooled connection string
  is used in production.

### Migrations

- Alembic is the only path to schema changes. Never run raw DDL by hand.
- One migration per PR. Migrations must be reversible.
- Migration filenames follow Alembic's `rev_<id>_<slug>.py` convention.

### Multi-Tenancy

- Every tenant-scoped table has a `tenant_id` column (UUID, FK to
  `businesses.id`, NOT NULL, indexed).
- A row-level tenant filter is enforced in the repository layer — never rely
  on the route to remember to filter.
- Cross-tenant access is a security incident and must be impossible through
  the public API.

### Naming

- Tables: `snake_case`, plural (`customers`, `purchase_invoices`).
- Columns: `snake_case`. Booleans prefixed with `is_` or `has_`.
- Foreign keys: `<singular>_id` (`customer_id`, `tenant_id`).
- Timestamps: `created_at`, `updated_at` (timestamptz, UTC).
- Primary keys: `id` UUID, default `gen_random_uuid()`.

## 5. Authentication Architecture

### Clerk

- Clerk is the identity provider. Billix never stores passwords.
- Frontend uses `@clerk/clerk-react` for sign-in / sign-up / session.
- Backend verifies the Clerk session JWT using Clerk's JWKS endpoint and
  the `clerk-backend-sdk` (or equivalent) inside the auth middleware.

### Flow

```
Browser ──(Clerk JWT in Authorization header)──▶ FastAPI
  │
  └─▶ AuthMiddleware (verifies JWT, extracts clerk_user_id)
        │
        └─▶ CurrentUserDependency (loads User row by clerk_user_id)
              │
              └─▶ TenantDependency (resolves active tenant from header)
                    │
                    └─▶ Route handler receives (current_user, tenant)
```

### Models

- `users` — mirrors Clerk users; `clerk_user_id` is unique.
- `businesses` — tenants.
- `business_memberships` — join table between users and businesses with a
  role enum.

### Roles

Roles are defined in `business_memberships.role`:

- `owner` — full control, billing access.
- `admin` — everything except billing.
- `accountant` — invoices, payments, reports.
- `staff` — limited to assigned module scope.

Roles are enforced in the service layer, not only in the UI.

## 6. Naming Conventions

### Frontend

- Components / files: `PascalCase` for components, `camelCase` for hooks and
  utilities.
- Hooks prefixed with `use`.
- Types / interfaces: `PascalCase`.
- API hooks: `use<Module><Action>Query` / `use<Module><Action>Mutation`.

### Backend

- Modules / files: `snake_case`.
- Classes: `PascalCase`.
- Functions / variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Pydantic schemas: `<Resource>Read`, `<Resource>Write`, `<Resource>Update`.

## 7. Coding Standards

- **Type safety first.** No `any` in TypeScript, no untyped `dict` returns in
  Python. Validate at boundaries.
- **No silent failures.** Log and surface errors; never swallow an exception
  and return `null`.
- **No magic strings.** Enums and constants live in dedicated files.
- **No commented-out code.** Delete it; rely on version control.
- **No premature abstraction.** Three concrete call sites before extracting
  a helper.
- **Tests required for services and repositories.** Routes are covered by
  integration tests.
- **Linting/formatting** — Prettier + ESLint on the frontend, Ruff + Black on
  the backend. CI fails on violations.
- **Commit messages** — `<ticket-id>: <imperative summary>` (e.g.
  `AUTH-003: add user model`).

## 8. Dependency Flow

```
Clerk ──▶ Frontend (auth state, JWT)
                  │
                  ▼
            FastAPI (auth middleware, current_user, tenant)
                  │
                  ▼
              Services ──▶ Repositories ──▶ PostgreSQL (Neon)
                  │
                  ├──▶ Appwrite (file storage for invoices, documents)
                  └──▶ Sentry (error reporting)
```

External integrations (GST e-invoice, payment gateways) are wrapped behind
service interfaces so they can be swapped without touching routes.

## 9. Design Principles

1. **Tenant isolation is non-negotiable.** Every query is tenant-scoped.
2. **Business logic lives in services.** Routes stay thin.
3. **Schemas are the contract.** Pydantic schemas are the public API; models
   are internal.
4. **Idempotency where it matters.** Payment recording, invoice numbering,
   and migration jobs must be idempotent.
5. **Observability by default.** Structured logs, request IDs, Sentry spans.
6. **Backwards-compatible migrations.** Add columns first, deploy, then
   read/write. Drop columns only after a release cycle.
7. **Security at the boundary.** Validate input on the way in; trust internal
   calls.
8. **Small, reversible changes.** One ticket, one PR, one migration.

## 10. What Should Never Be Modified Without Approval

The following are load-bearing decisions. Changing them silently can break
tenancy, billing, or compliance. **Require explicit human approval before
modifying:**

1. The multi-tenancy model — `tenant_id` columns, tenant filtering in
   repositories, and the tenant middleware.
2. The authentication flow — Clerk integration, JWT verification, the
   `current_user` dependency, and role definitions.
3. The migration framework — switching away from Alembic or disabling
   migrations.
4. The invoice numbering and GST calculation logic — these have legal
   implications.
5. The database engine choice (PostgreSQL/Neon) and connection pooling
   configuration.
6. The deployment targets (Vercel / DigitalOcean / Neon) and the release
   pipeline.
7. The public API contract — Pydantic response schemas and route paths under
   `/api/v1`.
8. The shadcn/ui base components in `src/components/ui/` — these are
   managed by the CLI.
9. The error envelope shape returned by the API.
10. The role enum and its permissions matrix.

If an AI assistant believes one of these needs to change, it must stop and
request approval with a written rationale before proceeding.
