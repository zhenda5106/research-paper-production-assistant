# Research Paper Production Assistant

**A research toolbox for choosing the skill you need, when you need it.**

Read a paper, check an analysis, draft a section, improve a figure, or prepare for a lab meeting from one place. Use each skill independently or start a preset workflow that connects several stages.

## Why I built this

I started this project while learning how to write research papers. Along the way, I found many useful AI skills: some helped with reading papers, others with statistics, academic writing, figures, or peer review. They covered different parts of the process, but were scattered across separate repositories.

I wanted to bring them together in a toolkit that I could use without searching for the right skill and setting everything up again each time. This project collects those skills, adds a shared entry point, and provides shortcuts for common research tasks.

I am still learning, and this is a tool I want to improve as I use it. The underlying skills belong to their respective authors; my contribution is organizing them and making them easier to use together.

## Quick start

### 1. Download the toolbox

Use **Code → Download ZIP** on GitHub and extract it, or clone it:

```bash
git clone https://github.com/zhenda5106/research-paper-production-assistant.git
cd research-paper-production-assistant
```

You need **Python 3.10 or newer**. The launcher itself uses only the Python standard library. On macOS/Linux, use `python3` if `python` is unavailable.

### 2. Open the menu

On Windows, double-click **`start.bat`**. On any supported platform:

```bash
python rppa.py
```

Choose a skill or workflow, enter your research project directory and task, and optionally provide an input file. The menu offers to download the required provider if it is missing.

Then choose how to continue:

- **Save a task prompt:** creates a Markdown task file for a local-file-capable desktop agent. Give that file to the agent to start the work.
- **Launch Codex CLI:** opens an interactive Codex session in your project with the prepared task. Codex must already be installed and authenticated; your account's normal usage terms apply.

Saving a prompt prepares the task; it does not generate a paper, run statistics, or create slides by itself. Both modes use the same task instructions and selected skills.

### 3. Optional: install named skills in your research project

Prepare the providers, create a project, and install the shortcuts:

```bash
python rppa.py setup
python rppa.py init ../my-paper
python rppa.py install --project ../my-paper --host codex
```

Open `my-paper` in Codex and invoke a skill directly:

```text
$rppa-read Read inputs/paper.pdf and explain the main contribution and limitations.
$rppa-polish Improve manuscript/introduction.md while preserving its claims.
$rppa-review Review manuscript/draft.md for unsupported conclusions.
```

For Claude Code, use:

```bash
python rppa.py install --project ../my-paper --host claude
```

Then invoke `/rppa-read`, `/rppa-polish`, or another installed skill in Claude Code. Project skills follow the host's native discovery conventions; see the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

The installer creates nine small project-level entrypoints. It does not change your global skills or overwrite unrelated existing ones. These entrypoints point to your local toolbox: keep it in place, and re-run `install` if you move it. The host must be allowed to read that directory. Reopen or refresh the project after installation if necessary.

## Choose a skill

| Shortcut | Upstream skill | What to use it for | Useful inputs | Expected work products |
|---|---|---|---|---|
| `ideas` | Brainstorming Research Ideas | Explore research questions and compare possible directions | Field, initial ideas, constraints | Candidate questions, rationale, feasibility considerations |
| `read` | Nature Reader | Read a paper closely, explain a passage, or build source-linked notes | PDF, DOI, URL, text | Reading notes or a reader, evidence locations, limitations |
| `stats` | Statistical Analysis | Choose methods, examine assumptions, or audit reported statistics | Dataset, study design, analysis code or manuscript | Analysis/checking report, estimates and uncertainty when data permit |
| `write` | Academic Paper | Plan a paper or draft and revise specific sections | Research question, verified results, references | Outline, section draft, revision or response-letter draft |
| `polish` | Nature Polishing | Improve academic expression without changing the findings | Draft text, target section and venue | Revised prose with material ambiguities flagged |
| `figure` | Nature Figure | Plan and produce manuscript figures, panels and schematics | Data or draft figure, intended message, Python/R preference | Figure files, generating code and captions where applicable |
| `visualize` | Scientific Visualization | Choose honest data encodings, display uncertainty and improve readability | Dataset and variable definitions | Plots, plotting code and export checks |
| `review` | Academic Paper Reviewer | Critique a manuscript or verify whether revisions address comments | Manuscript, target venue, reviewer comments | Located findings, revision priorities or re-review results |
| `slides` | Nature Paper2PPT | Turn a paper or reading notes into a presentation | Paper, audience, duration and language | Deck and speaker notes, subject to available document tools |

The installed names add `rppa-` to these shortcuts: `rppa-ideas`, `rppa-read`, `rppa-stats`, `rppa-write`, `rppa-polish`, `rppa-figure`, `rppa-visualize`, `rppa-review`, and `rppa-slides`.

You can also use an upstream name in terminal commands, such as `nature-reader` instead of `read`. Output language defaults to English through the orchestration layer; specify another language in your task when needed.

## Everyday commands

Run these commands from the toolbox directory. Replace the example project and input paths with your own. Relative paths are resolved from the terminal's current directory.

### Inspect the toolbox and environment

```bash
python rppa.py list
python rppa.py doctor
```

`list` shows the skills, required inputs and download status. `doctor` also checks for Codex CLI, common document tools and selected scientific Python packages. Discovery does not verify authentication or guarantee a working scientific runtime.

### Download only what you need

```bash
python rppa.py setup read
python rppa.py setup stats visualize
```

Or prepare every provider:

```bash
python rppa.py setup
```

Skills from the same provider share one download. Provider snapshots preserve their full repository layout so shared references continue to work. The download step does not install Python/R packages or run upstream code.

### Create a research workspace

```bash
python rppa.py init ../my-paper
```

This creates `inputs/`, `notes/`, `analysis/`, `manuscript/`, `figures/`, `slides/`, `reviews/`, and `outputs/`, plus a short `PROJECT.md` brief. Existing files are preserved. Put your source materials in this project rather than inside the toolbox dependencies.

### Prepare a single task

```bash
python rppa.py run read --project ../my-paper --input ../my-paper/inputs/paper.pdf --task "Explain the research question, methods, strongest evidence and limitations."
```

The default saves a task file under `<project>/.rppa/tasks/`. Open it with your desktop agent. For an interactive Codex launch, add `--agent codex`:

```bash
python rppa.py run polish --project ../my-paper --input ../my-paper/manuscript/introduction.md --task "Polish this introduction in English; preserve citations and claim strength." --agent codex
```

Repeat `--input` to include more than one file. Each task receives a separate prompt file, so earlier tasks are retained. The agent is asked to save new deliverables in `<project>/outputs/` and preserve original materials.

## Preset workflows

These are shortcuts for preparing a coordinated agent task. They do not bypass missing evidence, tool requirements or the host's permissions.

### Paper to presentation

**Paper reading → presentation**

Build source-linked reading notes, then use them to create a presentation with evidence figures, limitations and speaker notes.

```bash
python rppa.py workflow paper-to-slides --project ../my-paper --input ../my-paper/inputs/paper.pdf --task "Prepare a 15-minute English journal-club presentation for first-year PhD students." --agent codex
```

### Pre-submission check

**Statistics → peer review → language polishing**

Check statistical reporting, examine the argument and supporting evidence, then polish supported statements. With manuscript-only input, the statistics stage is a reporting audit, not a reanalysis of the data.

```bash
python rppa.py workflow submission-check --project ../my-paper --input ../my-paper/manuscript/draft.md --task "Check this methods paper before submission. List issues that need author decisions."
```

### Reviewer response and revision

**Review comments → manuscript revision and response → verification**

Map comments to concrete actions, revise using the available evidence, draft point-by-point responses, and check that the responses match the revised manuscript. Proposed experiments remain separate from completed work.

```bash
python rppa.py workflow revision --project ../my-paper --input ../my-paper/manuscript/draft.md --input ../my-paper/reviews/comments.md --task "Address these comments and prepare a response letter. Flag changes that require new experiments."
```

For any workflow, omit `--agent codex` to prepare a prompt file instead of launching the CLI. If dependencies are missing, the command prints the corresponding `setup` command; the interactive menu can prepare them for you.

## What you need beyond the launcher

- An AI agent with permission to read your local research files and toolkit.
- A configured model account for that agent. RPPA does not supply API credentials or a model subscription.
- Task-specific libraries and tools. Statistical analysis, rendering figures, reading scanned PDFs, and creating PPTX files may require additional Python packages, R, OCR or document renderers. Some providers require a newer Python version than the launcher.
- Actual research materials. A skill cannot replace missing measurements, unperformed experiments or inaccessible source text.

The menu, generated prompts and installed entrypoints are English. Upstream files retain their original text and licenses. The direct CLI launcher currently targets Codex; Claude Code is supported through project skills and prompt files.

## Troubleshooting

| Situation | What to do |
|---|---|
| Python is not found | Install Python 3.10+ and reopen your terminal; try `python3` on macOS/Linux or `py -3` on Windows. |
| A skill says it is not downloaded | Run `python rppa.py setup <shortcut>`, or let the menu prepare it. |
| Codex CLI is not found | Use prompt-file mode with a desktop agent, or install and authenticate Codex separately. |
| A new skill is not visible | Reopen the research project; confirm you selected the right host and that it can read the toolbox directory. |
| You moved the toolbox | Run `install` again against each project to refresh the local paths. |
| A download fails | Check GitHub access and rerun setup. Completed providers are reused. A partial directory without a receipt is not overwritten automatically; move that provider directory aside before retrying. |
| A figure or deck cannot be rendered | Check `doctor` and the selected skill's runtime requirements. A prompt file is not a rendered artifact. |

## Credits and licensing

This toolkit brings together work by:

- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills): paper reading, polishing, figures and presentations; Apache-2.0 at the repository root.
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills): statistical analysis and scientific visualization; MIT.
- [KalarisLabs/research-agent-skills](https://github.com/KalarisLabs/research-agent-skills): the selected research-ideation distribution; MIT, with upstream credit to [orchestra-research/AI-research-SKILLs](https://github.com/orchestra-research/AI-research-SKILLs).
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills): academic writing and peer review; **CC BY-NC 4.0**.

The original launcher, orchestration and documentation are [MIT licensed](LICENSE). Third-party terms remain in force. **The full configured toolkit includes noncommercial components**; the MIT license does not make those components commercially unrestricted. Nature Figure assets with unresolved permissions are excluded from extraction.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution and exceptions. The project is not affiliated with or endorsed by Nature, Springer Nature, or the upstream authors. Local dependency snapshots and research materials are not included in the Git release.

## Development and verification

```bash
python -m unittest discover -s tests -v
python scripts/validate.py
```

The structural validator requires all four providers to be downloaded. Tests cover routing, task preparation, missing inputs, project installation, preservation of existing files and CLI dispatch without starting a model. Scientific quality and document rendering still require real-task evaluation; this project does not claim end-to-end validation of every upstream workflow.

To suggest improvements, [open an issue](https://github.com/zhenda5106/research-paper-production-assistant/issues) with the task you were trying to complete and what would make it easier. Please keep unpublished or sensitive research data out of public issues.
