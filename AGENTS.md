# AGENTS.md

Docssistant is a document chat assistant that uses retrieval-augmented generation to answer questions with source citations. It uses FastAPI and Python 3.12+, PostgreSQL with SQLAlchemy and Alembic, Chroma for vector search, and a React 19 frontend built with TypeScript and Vite. Use Node 24+ and pnpm 10.3.0 for JavaScript tooling.

## Repository layout

- `api/` contains FastAPI routes grouped by feature (for example `api/conversations/`). Follow the existing feature modules for their split of `routes.py`, `requests.py`, `responses.py`, `dtos.py`, `services.py`, `repositories.py`, `models.py`, and `errors.py`.
- `indexer/` contains the worker that scans and indexes documents. Raw documents are read from the local `.documents/` directory in development.
- `libs/` contains shared domain code and infrastructure clients used by the API and indexer. `libs/defaults/` holds the base classes (`BaseController`, `BaseService`, plus shared models, repositories, requests, responses, and errors) that feature modules extend; `libs/application/` holds cross-cutting enums, DTOs, errors, and dependency providers.
- `migrations/versions/` contains Alembic revisions. Pair SQLAlchemy schema changes with an Alembic migration and review the generated upgrade and downgrade.
- `web/` contains the React and Vite frontend. See the frontend section below for its layout and conventions.
- `test/unit/` and `test/integration/` contain pytest tests. Shared mocks live in `test/mocks/`.
- `deployments/` contains Docker Compose configurations and `build/package/` contains Dockerfiles.

## Commands

Run commands from the repository root.

| Command                                                           | Purpose                                                                         |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `make install`                                                    | Install pnpm dependencies and Python dependencies into `.venv`.                 |
| `make dev`                                                        | Build and start the development stack with Docker Compose and `.env.dev`.       |
| `pnpm dev` / `pnpm build`                                         | Start the Vite dev server or build the frontend.                                |
| `pnpm exec tsc --noEmit --incremental false -p web/tsconfig.json` | Type-check the frontend.                                                        |
| `make lint_py`                                                    | Run Flake8.                                                                     |
| `make test_py_unit`                                               | Run Python unit tests.                                                          |
| `make test_py_integration`                                        | Run integration tests with Docker Compose, PostgreSQL, Chroma, and `.env.test`. |
| `make test`                                                       | Run the integration and unit suites.                                            |
| `make create_migration MESSAGE="describe schema change"`          | Generate an Alembic revision using the development stack.                       |
| `make migrations_upgrade_dev` / `make migrations_downgrade_dev`   | Apply pending development migrations or roll back one revision.                 |

## Frontend

### Layout

- `web/src/main.ts` bootstraps React, logging, and i18next.
- `web/src/platform/` contains shared frontend infrastructure, organised the same way a feature is:
  - `platform/application/` is the app's own platform layer: the app shell (`containers/App/`), the shared UI component library (`components/`, see "Compound components" below), and shared `hooks/`, `services/`, `enums/`, `types/`, and `utilities/` (such as the `cn()` class-merging helper).
  - `platform/defaults/` holds base classes shared by services, such as `BaseAPIService` and `BaseError`.
  - `platform/http/` holds shared HTTP error types (`ValidationError`, `ParsingError`, `InternalServerError`).
  - `platform/logging/` holds the `createLogger` utility, and `platform/translations/` holds the i18next resources.
- Put product code in `web/src/<feature>/` as features are added (`conversation/` is the current example). Organise each feature by the layers it uses, such as `containers/`, `components/`, `hooks/`, `services/`, `enums/`, `errors/`, or `types/`. Containers compose the feature UI, components render props, hooks manage React state and effects, and services handle API calls.
- Keep feature-specific code in its feature. Share code between features through public exports. Platform modules can be used by features. The app shell can compose features while shared infrastructure such as logging stays independent of them.
- Styling uses Tailwind CSS v4 (via `@tailwindcss/vite`) with a shadcn-style CSS-variable theme (see `platform/styles/global.css`). Shared UI primitives in `platform/application/components/` are adapted from shadcn/prompt-kit; merge class names with the `cn()` utility rather than concatenating strings.

### Anatomy of a unit

For a component owned by the chat feature, use a structure like this:

```text
web/src/conversation/components/SourceLink/
├── SourceLink.tsx        # Default export named SourceLink
├── SourceLink.test.tsx   # Colocated test when covered by a frontend test runner
├── index.ts              # Public exports for the unit
├── types/
│   ├── Props.ts          # Default export named Props
│   └── index.ts          # export type { default as Props } from './Props';
└── utilities/            # Optional unit-private helpers
    ├── formatSourceLabel.ts
    └── index.ts
```

- Keep `index.ts` files limited to re-exports. The unit barrel exports its default implementation and any types or other members intended for callers. Private helpers stay inside the unit.
- Put type declarations in `types/`, one per file, with names such as `Props`, `HeaderProps`, or `UseChatState`. Add unit-local directories such as `components/`, `hooks/`, or `utilities/` when the unit needs them. Move helpers used by multiple units to their nearest shared feature or platform module.
- Colocate frontend tests as `Name.test.ts` or `Name.test.tsx` when a frontend test runner is available (none is wired up yet, so there are no `*.test.*` files today).

#### Compound components

When a unit is made of several nested parts (for example `platform/application/components/Message/` or `Tooltip/`), attach the parts to the main component with dot notation instead of exporting them separately:

```text
web/src/platform/application/components/Message/
├── Message.tsx            # const Message: Component<Props> = (...) => (...);
│                           # Message.Avatar = Avatar; Message.Content = Content; ...
├── index.ts                # export { default } from './Message'; export * from './components'; export * from './types';
├── components/
│   ├── Avatar.tsx
│   ├── Content.tsx
│   └── index.ts
└── types/
    ├── Component.ts        # interface Component<Props> extends FC<Props> { Avatar: FC<AvatarProps>; Content: FC<ContentProps>; }
    ├── Props.ts
    ├── AvatarProps.ts
    └── index.ts
```

Callers then write `<Message.Avatar>` / `<Message.Content>` rather than importing separate named components. Use a plain `as Component<Props>` cast for non-ref-forwarding roots (such as Radix's `TooltipPrimitive.Root`), and `as unknown as Component<Props>` for `forwardRef`-based roots (such as `Avatar`), since TypeScript rejects the direct cast there as an insufficient overlap. Reserve this pattern for genuinely multi-part units; a single-purpose component (`Button`, `Textarea`, `Loader`) stays a plain default export.

### Imports and code conventions

- Between units, use `@/` (which resolves to `web/src/`) and import through the unit barrel, for example `@/platform/logging/utilities/createLogger`. Within a unit, use relative imports such as `./types` and `../types`.
- Put third-party imports first. Group project imports under lowercase role headers such as `// components`, `// containers`, `// enums`, `// errors`, `// hooks`, `// services`, `// ui`, `// utilities`, and `// types`, in alphabetical order. In feature code, use `// ui` for imports from the shared `platform/application/components/` library, to keep them visually distinct from the unit's own feature-local `// components`. Use `import type` for type-only imports.
- Use PascalCase directories and filenames for components and containers. Define components as typed function components with default exports, as in the existing `App` unit.
- Name hooks `useX`, default-export them, and put their return types in `types/` when a named type is needed. For longer hooks, use section comments in this order where applicable: `// contexts`, `// hooks`, `// refs`, `// states`, `// memos`, `// callbacks`, `// effects`.
- Use i18next and the resources in `platform/translations/` for user-facing strings. Run the TypeScript check and Vite build for frontend changes.

## Repository conventions and verification

- Use isort and Black for Python and Prettier for TypeScript and Markdown. Prefer formatting only the files you changed. `make format` formats across the repository.
- Keep HTTP handling in route modules, application logic in services, and persistence in repositories. Reuse the existing dependency providers and shared models.
- Use `.env.example` as the reference for configuration variables. Keep credentials and private documents out of commits.
- Cover Python behaviour changes in the appropriate pytest suite. Pull request CI runs Flake8 and both Python suites.
- Follow [CONTRIBUTING.md](./CONTRIBUTING.md) for branch names, conventional commits, and pull request titles. Keep Git hooks enabled.
