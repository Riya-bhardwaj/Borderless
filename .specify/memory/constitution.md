<!--
  Sync Impact Report
  ==================
  Version change: 1.0.0 → 1.1.0
  Modified principles: None renamed
  Added sections:
    - Principle VII. Beautiful & Intuitive UX (new)
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ compatible (Constitution Check section present)
    - .specify/templates/spec-template.md ✅ compatible (user scenarios support UX-driven validation)
    - .specify/templates/tasks-template.md ✅ compatible (phase structure supports UX tasks)
  Follow-up TODOs: None
-->

# Borderless Constitution

## Core Principles

### I. Modern Practices

All code MUST follow current industry best practices and conventions for the
chosen language and framework. This includes:

- Use the latest stable language features and idioms
- Follow official style guides and linting rules for the language/framework
- Prefer well-maintained, widely-adopted libraries over custom solutions
- Use modern tooling (package managers, formatters, linters, type checkers)
- Keep dependencies up to date and audit for vulnerabilities

**Rationale**: Modern practices reduce technical debt, improve developer
experience, and ensure long-term maintainability.

### II. Configuration-Driven Design

All feature behavior, settings, and toggles MUST be externalized into
configuration files (JSON, YAML, or ENV) rather than hardcoded in source code.

- Feature flags, thresholds, labels, and messages MUST live in config files
- Environment-specific values (URLs, keys, ports) MUST use `.env` files
- Structured configuration (schemas, mappings, rules) MUST use JSON or YAML
- Every config file MUST have a corresponding schema or validation
- Config files MUST be documented with inline comments or a companion README
- Sensible defaults MUST be provided so the app runs without custom config

**Rationale**: Configuration-driven design enables non-developers to modify
application behavior without touching source code, and supports multiple
deployment environments without code changes.

### III. Extensibility & Modularity

Code MUST be structured so that features can be added, removed, or modified
independently without understanding the entire codebase.

- Each feature MUST be a self-contained module with clear boundaries
- Modules MUST communicate through well-defined interfaces, not internal state
- Plugin or registry patterns SHOULD be used where features are enumerable
- New features MUST be addable by creating a new module and a config entry
- Shared utilities MUST be extracted into common libraries when used by 3+ modules
- Dependencies between modules MUST be explicit and unidirectional

**Rationale**: Modularity enables parallel development, reduces cognitive load,
and allows non-experts to contribute by working within isolated boundaries.

### IV. Quality-First Testing

Every feature MUST have comprehensive tests before it is considered complete.

- Unit tests MUST cover all public functions and edge cases
- Integration tests MUST verify module interactions and data flow
- Contract tests MUST validate API boundaries and external interfaces
- Test coverage MUST NOT decrease with any change
- Tests MUST be deterministic, fast, and independent of external state
- Test names MUST describe the behavior being verified in plain language

**Rationale**: Comprehensive testing is the primary mechanism for ensuring
code quality and preventing regressions. Tests serve as living documentation
of expected behavior.

### V. Non-Breaking Changes (NON-NEGOTIABLE)

No change MUST break existing functionality. This is the highest-priority
principle and overrides all others when in conflict.

- All changes MUST pass the full existing test suite before merge
- API changes MUST be backward-compatible or versioned with a migration path
- Database schema changes MUST use additive migrations (no destructive ALTER/DROP)
- Config file changes MUST be backward-compatible with existing config files
- Deprecated features MUST continue to function for at least one major version
- Every PR MUST include a "Breaking Change Assessment" confirming no regressions

**Rationale**: Stability is the foundation of trust. Users, integrations, and
dependent systems MUST be able to rely on existing behavior continuing to work.

### VI. Simplicity & Accessibility

Code MUST be written so that someone unfamiliar with the codebase can
understand, modify, and extend it with minimal onboarding.

- Prefer explicit code over clever abstractions
- Functions MUST do one thing and be named to describe that thing
- Complex logic MUST be broken into small, well-named helper functions
- Directory structure MUST mirror the feature/domain structure
- README files MUST exist at the project root and for each major module
- Avoid deep inheritance hierarchies; prefer composition and flat structures

**Rationale**: Accessibility lowers the barrier to contribution and reduces
the bus factor. Code that is easy to understand is easy to maintain.

### VII. Beautiful & Intuitive UX

Every screen, interaction, and transition MUST deliver a polished, visually
beautiful, and effortlessly intuitive user experience following modern
Android design principles.

- All UI MUST follow Material Design 3 (Material You) guidelines including
  dynamic color theming, typography scales, and elevation hierarchy
- Navigation MUST follow Android platform conventions (bottom navigation,
  predictive back gestures, edge-to-edge content)
- Every user-facing interaction MUST include smooth, purposeful animations
  and transitions (shared element transitions, motion choreography)
- Touch targets MUST meet minimum 48dp sizing; spacing and padding MUST
  follow the 8dp grid system
- The app MUST support dark mode, dynamic color (Material You wallpaper
  theming), and responsive layouts for all screen sizes
- Typography MUST use a clear visual hierarchy with no more than 3 type
  scales per screen
- Loading states, empty states, and error states MUST be designed with the
  same care as primary content screens
- User flows MUST be completable with minimal taps; every unnecessary step
  MUST be eliminated
- Accessibility MUST be built-in: sufficient color contrast (WCAG AA),
  content descriptions for screen readers, and scalable text support

**Rationale**: The app serves travelers in unfamiliar, potentially stressful
situations. A beautiful and intuitive interface builds trust, reduces
cognitive load, and ensures critical information is consumed quickly and
without confusion.

## Configuration & Extensibility Standards

- **Config file locations**: All config files MUST reside in a `config/`
  directory at the project root, organized by concern (e.g., `config/features/`,
  `config/env/`, `config/schemas/`)
- **Config format selection**:
  - `.env` for environment variables and secrets
  - `.json` for structured data with schema validation
  - `.yaml` for human-readable configuration with comments
- **Schema validation**: Every JSON/YAML config file MUST have a corresponding
  JSON Schema that validates its structure at startup
- **Hot reload**: Where feasible, config changes SHOULD take effect without
  restarting the application
- **Feature registration**: New features MUST be registerable via config
  without modifying core application code

## Quality Gates & Development Workflow

- **Pre-commit**: Linting, formatting, and type checking MUST pass
- **Pre-merge**: Full test suite MUST pass with no coverage decrease
- **Code review**: Every change MUST be reviewed by at least one other person
  or validated by automated analysis
- **Regression check**: Every PR MUST demonstrate that existing tests pass
  unchanged (no test modifications to "fix" failing tests unless the test
  itself was incorrect)
- **Documentation**: Public APIs and config options MUST be documented before
  merge

## Governance

This constitution is the highest authority on development practices for the
Borderless project. All code, PRs, and architectural decisions MUST comply
with these principles.

- **Amendments**: Any change to this constitution MUST be documented with
  rationale, reviewed, and versioned using semantic versioning
- **Version policy**: MAJOR for principle removals/redefinitions, MINOR for
  new principles or material expansions, PATCH for clarifications and wording
- **Compliance**: All PRs and reviews MUST verify compliance with these
  principles. Non-compliance MUST be justified and documented in the PR
- **Conflict resolution**: When principles conflict, priority order is:
  V (Non-Breaking) > IV (Testing) > VII (UX) > II (Config-Driven) >
  III (Modularity) > I (Modern Practices) > VI (Simplicity)

**Version**: 1.1.0 | **Ratified**: 2026-02-14 | **Last Amended**: 2026-02-14
