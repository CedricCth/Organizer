# Todos feature — worked example

This folder is the canonical example of how a feature is structured in this codebase.
**Read this once**, then mirror the structure when building any new feature
(auth, couple, recurring tasks, ...).

## Layer map

```
todos/
├── domain/                   pure TS, no framework imports
│   └── Todo.ts               entity, value types, validation rules, pure status transitions
├── application/              use cases + repository interface (DI seam)
│   ├── TodoRepository.ts     interface — owned by this layer
│   ├── createTodo.ts         use case factory
│   ├── listTodos.ts          use case factory
│   └── toggleTodo.ts         use case factory (read-modify-write demo)
├── adapters/                 framework / Supabase / HTTP boundary
│   ├── SupabaseTodoRepository.ts   implements TodoRepository
│   ├── schema.ts             Zod schemas for incoming form data
│   ├── actions.ts            Next.js server actions — thin
│   └── composition.ts        composition root: wires real impls into use cases
├── ui/                       React components (shadcn/ui based) — to be added
└── __tests__/
    └── createTodo.test.ts    use case test using a fake repo (no Supabase)
```

## Reading order if you're new

1. `domain/Todo.ts` — what a Todo is, what its rules are.
2. `application/TodoRepository.ts` — the interface use cases depend on.
3. `application/createTodo.ts` — pattern for a use case factory.
4. `adapters/SupabaseTodoRepository.ts` — how the interface is implemented.
5. `adapters/composition.ts` — how it's all wired.
6. `adapters/actions.ts` — how the HTTP boundary calls into it.
7. `__tests__/createTodo.test.ts` — payoff: testable in isolation.

## Adding a new use case

1. Add a method to `TodoRepository` if the new use case needs a new query.
2. Implement the method in `SupabaseTodoRepository`.
3. Write the use case factory in `application/yourUseCase.ts`.
4. Wire it into `composition.ts`.
5. Expose it via a server action in `actions.ts` (and a Zod schema in `schema.ts`).
6. Write a unit test using the fake repo pattern.

If you find yourself wanting to import `@supabase/supabase-js` from inside `application/` or `domain/` — stop. Add a method to the repository instead.
