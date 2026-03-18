# Adapter: React + Node Monorepo

Use this when the target project has a front-end app, an API app, and shared packages.

## Recommended `.aidrp/config.json` Adjustments

- Add `apps/web/src/main.tsx` and `apps/api/src/index.ts` to preferred entry files.
- Add validation commands for `quick`, `precommit`, and `ship`.
- Mark `packages/shared/` as high-signal for schema and type work.

## Common Read Order

1. `README.md`
2. `AGENTS.md`
3. `package.json`
4. `apps/web/package.json`
5. `apps/api/package.json`
6. `packages/shared/*`
7. task packet shortlist

## Common Risk Areas

- cross-package type drift
- stale generated clients
- mismatched environment variable handling
- front-end cache invalidation after API changes
