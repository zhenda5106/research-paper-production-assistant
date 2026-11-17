# Third-party sources and boundaries

Checked 2026-11-17. This public project contains original orchestration and a dependency fetcher. Third-party implementation files are downloaded separately into `.upstream/` and are not included in the intended Git distribution. Retained files are not edited; the Nature snapshot has the exclusion below. Full commits and archive hashes are in `sources.lock.json`.

| Local ID | Upstream | Selected work | Terms and notices |
|---|---|---|---|
| nature | https://github.com/Yuan1z0825/nature-skills | nature-reader, nature-polishing, nature-figure, nature-paper2ppt and shared resources | Root LICENSE: Apache-2.0; individual assets can have different terms. Preserve upstream authorship. |
| ideas | https://github.com/KalarisLabs/research-agent-skills | brainstorming-research-ideas | Copyright (c) 2026 Kalaris Labs; MIT. Preserve LICENSE, THIRD_PARTY_NOTICES.md, LICENSES/ and provenance manifest. |
| scientific | https://github.com/K-Dense-AI/scientific-agent-skills | statistical-analysis, scientific-visualization | Copyright (c) 2025 K-Dense Inc.; MIT, in LICENSE.md. |
| academic | https://github.com/Imbad0202/academic-research-skills | academic-paper, academic-paper-reviewer and shared resources | Copyright (c) 2026 Cheng-I Wu; CC BY-NC 4.0. Preserve LICENSE, NOTICE.md and THIRD_PARTY.md. |

## Ideas provenance

Kalaris Labs identifies brainstorming-research-ideas as adapted from [orchestra-research/AI-research-SKILLs](https://github.com/orchestra-research/AI-research-SKILLs), revision `773a52944ba4747a18bd4ae9ade53fff041adcbc`, copyright (c) 2025 Claude AI Research Skills Contributors, MIT. Its `LICENSES/MIT-upstream-b.txt` and `third_party/upstream-manifest.json` are retained in the local snapshot. Kalaris is the selected maintained distribution, not claimed as the sole original author.

## Excluded Nature Figure assets

The pinned Nature repository contains `skills/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md`. It identifies [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) and states that explicit permission was not established. Its mention of an older root MIT license does not override the current root Apache license or confer rights to those assets.

The integration excludes the entire `skills/nature-figure/assets/figures4papers/` directory during extraction and forbids using those assets through its router. No permission is inferred from attribution, public availability or free distribution. Other assets are not certified by this review; inspect their terms before copying them into publication outputs or redistributing a bundle.

## Noncommercial scope

The user selected free, noncommercial research sharing. CC BY-NC 4.0 permits sharing/adaptation subject to its terms; the original MIT orchestration does not remove that restriction from the Academic dependencies. A future commercial deployment requires a new assessment and, if needed, separate permission or replacement. Source linking and separate download do not make otherwise restricted use unrestricted.

Do not present the upstream authors or Nature/Springer Nature as endorsing this project. Do not include user papers, datasets, credentials or local caches in a public release.
