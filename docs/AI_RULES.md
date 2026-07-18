# Billix — AI Rules

> These rules are binding for every AI assistant working on Billix
> (Bolt AI, Cursor, Claude, ChatGPT, Jules, Trae, and any other agent).
> Read this file in full before touching any code.

## 1. Core Rules

1. **Never redesign the architecture.** The architecture described in
   `docs/ARCHITECTURE.md` is final. If you believe a change is warranted,
   stop and request approval with a written rationale.
2. **Never create demo code.** No mock data, no placeholder logic, no
   "TODO later" stubs. Every change must be production-ready.
3. **Never modify unrelated files.** Touch only the files required by the
   current ticket. Refactors, renames, and "while I'm here" cleanups are
   forbidden unless explicitly requested.
4. **Never implement future milestones.** Implement only the ticket
   assigned in the current prompt. Do not pre-build scaffolding for later
   milestones.
5. **Complete only one engineering ticket at a time.** Do not bundle
   tickets. If a change logically spans two tickets, stop and ask which to
   prioritize.
6. **Prefer reusable code.** Before adding a new utility, helper, or
   component, search the codebase for an existing one. Extend before you
   duplicate.
7. **Use production-ready coding practices.** Type-safe, validated at
   boundaries, no silent failures, no `any`/untyped dicts, no
   commented-out code, no dead exports.
8. **Maintain modular architecture.** Keep routes thin, services
   authoritative, repositories SQL-only. Do not leak layers.
9. **Follow the existing folder structure.** Place new files where a
   reader would expect them based on `docs/ARCHITECTURE.md`. Never invent
   a parallel hierarchy.
10. **Explain every file modification.** In your final summary, list each
    file touched and the reason. No silent edits.
11. **Stop after completing each ticket.** Do not chain into the next
    ticket. Summarize, then wait for the next instruction.
12. **Ask for clarification instead of making assumptions.** Ambiguity
    about scope, naming, or behavior must be raised as a question, not
    resolved silently.

## 2. What You Must Never Do

- Do not add authentication until explicitly requested.
- Do not create database models, migrations, or RLS policies outside the
  current ticket.
- Do not create routes, middleware, or APIs outside the current ticket.
- Do not introduce new dependencies without checking `package.json` /
  `pyproject.toml` and confirming with the user.
- Do not switch libraries (e.g., replace Clerk, replace Alembic, swap
  TailwindCSS).
- Do not edit shadcn/ui primitives in `src/components/ui/` by hand.
- Do not disable linting, formatting, or tests to make a change pass.
- Do not commit secrets, `.env` files, or local configuration.
- Do not force-push, rewrite published git history, or amend pushed
  commits.
- Do not modify the documentation files in `docs/` to retroactively
  justify a code change. If the docs are wrong, flag it.

## 3. Required Workflow Per Ticket

1. Read all four docs:
   - `docs/PROJECT_CONTEXT.md`
   - `docs/ARCHITECTURE.md`
   - `docs/ROADMAP.md`
   - `docs/AI_RULES.md`
2. Confirm the current ticket from `docs/ROADMAP.md` and verify it is the
   next uncompleted ticket in its milestone.
3. Read the relevant existing code before writing anything new.
4. Implement the smallest correct change that satisfies the ticket's
   completion criteria.
5. Run lint and tests. If something fails, fix the cause — do not paper
   over it.
6. Summarize:
   - Files created / modified / deleted (with one-line reasons).
   - How the ticket's completion criteria are met.
   - Any follow-up questions or risks.
7. Stop. Wait for the next instruction.

## 4. How Future Prompts Should Begin

Every future prompt that asks an AI assistant to implement work on Billix
**must** begin with the following block, verbatim:

```
Read the following documentation before implementing anything:

docs/PROJECT_CONTEXT.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/AI_RULES.md

Treat them as the single source of truth.
```

The prompt should then state:

- The exact ticket ID being implemented (e.g., `AUTH-003`).
- Any decisions already made by the human owner.
- Any constraints or preferences for this specific ticket.

## 5. Communication Style

- Be concise. No preambles, no recaps of the rules, no apologies.
- State decisions directly. "I did X because Y" — not "I considered
  several options and ultimately decided to…".
- Surface risks explicitly. If a change could affect tenancy, auth,
  billing, or compliance, call it out before making the change.
- When you stop, end with a clear handoff: what was done, what is
  unverified, and what you need from the human owner next.

## 6. When in Doubt

- **Stop and ask.** A 30-second clarification is always cheaper than a
  wrong implementation that has to be reverted.
- **Prefer the docs.** If code and docs disagree, trust the docs and flag
  the code.
- **Prefer reversibility.** Choose the change that is easiest to roll
  back.
- **Prefer the smallest diff.** A focused PR is easier to review and
  less likely to introduce regressions.
