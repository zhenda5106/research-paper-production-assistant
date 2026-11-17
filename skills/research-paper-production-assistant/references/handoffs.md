# Cross-stage handoffs

Use existing artifacts where possible. For a new multi-stage project, keep outputs under a user-selected project directory, not inside upstream dependencies.

| Handoff | Minimum content |
|---|---|
| Idea → reading/design | Research question, candidate contribution, feasibility constraints, assumptions and literature checks still needed. |
| Reading → writing | Source identifier, bibliographic verification status, relevant claim, supporting location, limitations and access level. |
| Analysis → figures/writing | Dataset version, design, sample definition, exclusions, method, assumptions, estimates/uncertainty, code and output paths. |
| Writing → polishing | Manuscript version, target section/venue, protected numbers and terms, intended claim strength. |
| Figures → manuscript | Figure file, generating script/data version, panel mapping, caption, export dimensions and completed QA. |
| Review → revision | Comment ID, manuscript location, issue, proposed action, author decision, changed location and evidence of resolution. |
| Paper → slides | Manuscript/source version, audience/duration, main argument, evidence figures, limitations and attribution. |

When a result changes, update affected captions, manuscript claims, abstracts and slides or explicitly list stale artifacts. Keep original data and author drafts intact. A statement based only on user input must not become “independently verified” when passed to another stage.
