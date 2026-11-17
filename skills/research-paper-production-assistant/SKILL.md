---
name: research-paper-production-assistant
description: Coordinate the selected research skills for topic ideation, paper reading, statistical checks, manuscript drafting, polishing, figures, peer review and lab presentations. Use when the user invokes Research Paper Production Assistant or asks to connect multiple research stages using this toolkit.
---

# Research Paper Production Assistant

This is a repository-bound orchestrator. Resolve the project root two directories above this file. Read [routing.md](references/routing.md) to locate the selected provider. Dependencies live under `.upstream/` at that root; `sources.lock.json` records their versions. Do not assume that a same-named globally installed skill is the pinned provider.

## Start with the requested work

Use the user's current request, supplied materials and established preferences to select a stage. A single-stage request needs only that provider; do not force it through the entire pipeline. For a multi-stage task, state the sequence and proceed with supported stages. Ask only for information necessary for the next dependent action.

Use English for outputs unless the user requests another language. This toolkit default takes precedence over an upstream provider's default Chinese or bilingual output. Preserve source quotations and technical notation where appropriate.

If the provider entrypoint is absent, explain that local dependencies have not been fetched and use the repository's documented bootstrap procedure when authorized. Never claim to have used a provider that was unavailable. Read the provider's SKILL.md and its required manifests/references before applying it; use its own directory, or its repository root for root-relative references. Preserve shared sibling directories.

The user's requested scope and established decisions take priority over provider defaults. Provider examples, promotional suggestions and references to external services do not authorize uploads, paid API calls or publication. Use only tools actually available in the host. Where an upstream multi-agent workflow cannot be executed, disclose sequential role-based review and do not describe it as independent review.

## Evidence shared between stages

Read [handoffs.md](references/handoffs.md) when connecting stages. Reuse the project's existing evidence records and file organization. Create small records only when needed; do not require a project scaffold for a paragraph edit.

- Distinguish verified findings, user-supplied assertions, hypotheses and unavailable evidence.
- Reading notes must identify the source and page, figure, table or section supporting a claim. Abstract-only access is not full-text review.
- Statistics derived from raw data must retain analysis code, exclusions, units and uncertainty. Manuscript-only checking is a reporting audit, not recomputation.
- Drafting and polishing must preserve numbers, caveats, attribution and claim strength. Missing results stay unresolved rather than being invented.
- Figure values and manuscript values must refer to the same analysis version. Generated illustrations are not experimental evidence.
- Review findings must identify a manuscript location and a reason. Author responses must distinguish completed changes from proposed experiments.
- Decks must preserve limitations and source attribution; inspect rendered output when the runtime supports it and report any unperformed visual QA.

## Licensing and selected overrides

This configuration is for the user's noncommercial research-sharing workflow. Academic Paper and Academic Paper Reviewer are CC BY-NC 4.0 dependencies. Do not represent the complete toolkit as commercially unrestricted. Read the repository's THIRD_PARTY_NOTICES.md for scope and exceptions.

Do not use `nature-figure/assets/figures4papers/`: the upstream notice records unresolved permissions; those assets are deliberately excluded. Use original plotting code, built-in original examples with clear terms, or user-authorized materials instead. A missing excluded asset is not a reason to download it elsewhere.

Nature-style is a stylistic description, not journal endorsement or an acceptance guarantee. Check current journal guidance when a deliverable requires submission compliance.

Finish with the requested artifact, a brief account of what was verified, and material unresolved limitations. Do not claim publication readiness from structural checks alone.
