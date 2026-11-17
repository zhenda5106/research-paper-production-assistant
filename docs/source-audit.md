# Source audit

Checked on 2026-11-17 against pinned repository files.

## Findings

- The nine selected skills come from four repositories. Academic Paper and Academic Paper Reviewer use the same upstream project so their shared resources remain compatible.
- Root license files were inspected directly. GitHub reported NOASSERTION for two repositories; their actual license texts identify MIT and CC BY-NC 4.0 respectively.
- Kalaris lists the ideation skill as adapted from orchestra-research. Both attribution layers are retained.
- Nature skills use manifests and sibling nature-shared resources. Academic skills use root-level shared/ and scripts/ resources. Full repository layout is retained locally.
- Nature Figure includes figures4papers scripts and previews with unresolved permissions. That directory is excluded during extraction; the root license does not establish permission for those assets.

## Distribution

The Git release contains original orchestration, tooling, documentation and source references. Upstream implementations are downloaded into an ignored local directory. Retained upstream files are unchanged. The configured academic workflow includes CC BY-NC dependencies and is intended for noncommercial research use.

Repository downloads do not enable every included skill. No upstream installation scripts or paid model calls are part of setup. This review is not a comprehensive copyright or security audit of every file in the upstream repositories.

## Validation boundaries

Launcher tests and structural validation do not prove scientific quality. Recomputed results, reference verification, rendered figures, revised responses and presentation quality require task-specific materials and checks. Direct CLI dispatch is tested with a mocked process; real model-driven workflows have not been evaluated end to end.

## Dependency updates

When changing a provider, recheck its licenses, notices, asset exceptions, shared paths and entrypoints before updating the pinned commit and archive hash. An offline redistribution of upstream files needs a separate review of the actual packaged material and its notices.
