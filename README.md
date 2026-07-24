# alc-programming

[![content validation](https://github.com/astrapi69/alc-programming/actions/workflows/validate-content.yml/badge.svg)](https://github.com/astrapi69/alc-programming/actions/workflows/validate-content.yml)
[![engine on npm](https://img.shields.io/npm/v/learn-content-engine?label=engine%20on%20npm)](https://www.npmjs.com/package/learn-content-engine)

The [Adaptive Learner](https://github.com/astrapi69/adaptive-learner)
content repository for **Programmierung** (programming): a Git repository
of plain lesson files that the app loads directly and no vendor can lock
away.

It ships three German-language knowledge sets (domain `programming`,
`domain_label` Programmierung) in ascending difficulty: a Python
beginners course and a two-part React series. This repository was
created from
[adaptive-learner-content-template](https://github.com/astrapi69/adaptive-learner-content-template),
which provides the schema mirror, validator, CI and authoring tooling
described below.

> **Herkunft:** Diese Sets lagen zuvor im offiziellen Content-Repo
> [`adaptive-learner-content`](https://github.com/astrapi69/adaptive-learner-content)
> (`python-basics`) und im Test-/Starter-Repo
> [`adaptive-learner-content-test`](https://github.com/astrapi69/adaptive-learner-content-test)
> (beide React-Sets) und wurden in dieses eigenständige Content-Repo
> verschoben (siehe `adaptive-learner-content#144`).

## Die Sets

Drei Sets, 28 Lektionen, Quell- und Zielsprache Deutsch. Empfohlene
Reihenfolge:

### Teil 1 — `sets/de/python-basics` (A1, 15 Lektionen)

Einführung in die Programmierung mit Python: von `print()` und Variablen
über Strings, Listen, Bedingungen und Schleifen bis zu Funktionen,
Dictionaries, Fehlerbehandlung, Modulen, Dateien und Comprehensions -
mit lauffähigen Code-Beispielen und erwarteter Ausgabe.

| # | Lesson | Titel |
|---|--------|-------|
| 01 | `01-erste-schritte.json` | Erste Schritte mit Python |
| 02 | `02-variablen-und-datentypen.json` | Variablen und Datentypen |
| 03 | `03-zahlen-und-operatoren.json` | Zahlen und Operatoren |
| 04 | `04-strings.json` | Strings — mit Text arbeiten |
| 05 | `05-listen.json` | Listen (Lists) |
| 06 | `06-bedingungen.json` | Bedingungen (if / elif / else) |
| 07 | `07-schleifen.json` | Schleifen (for & while) |
| 08 | `08-funktionen.json` | Funktionen (def) |
| 09 | `09-dictionaries.json` | Dictionaries (dict) |
| 10 | `10-tupel-und-mengen.json` | Tupel und Mengen (tuple & set) |
| 11 | `11-fehler-und-ausnahmen.json` | Fehler und Ausnahmen (try / except) |
| 12 | `12-module-und-imports.json` | Module und Imports |
| 13 | `13-dateien.json` | Dateien lesen und schreiben |
| 14 | `14-comprehensions.json` | List Comprehensions |
| 15 | `15-wiederholung.json` | Wiederholung und Festigung |

### Teil 2 — `sets/de/react-grundlagen` (A2, 5 Lektionen)

| # | Lesson | Titel |
|---|--------|-------|
| 01 | `01-was-ist-react.json` | Was ist React? Library, Komponenten & deklarative UI |
| 02 | `02-jsx.json` | JSX verstehen: kein HTML, Ausdrücke in geschweiften Klammern |
| 03 | `03-props.json` | Props: Daten von Eltern an Kind, read-only & unidirektionaler Fluss |
| 04 | `04-state-usestate.json` | State mit useState: Re-Render statt direkter Mutation |
| 05 | `05-events-und-grundprinzipien.json` | Events, Hooks & Grundprinzipien: Re-Render und Komposition |

### Teil 3 — `sets/de/react-fortgeschritten` (B1, 8 Lektionen)

| # | Lesson | Titel |
|---|--------|-------|
| 01 | `01-useeffect-verstehen.json` | useEffect verstehen |
| 02 | `02-datenfetching.json` | Datenfetching-Grundmuster |
| 03 | `03-usecontext.json` | useContext |
| 04 | `04-useref.json` | useRef |
| 05 | `05-performance.json` | Performance: Re-Render, useMemo, useCallback |
| 06 | `06-listen-keys.json` | Listen und Keys |
| 07 | `07-formulare.json` | Formulare: controlled vs. uncontrolled |
| 08 | `08-komposition-patterns.json` | Komposition und Patterns |

## What's inside

- `manifest.yaml` — the root manifest listing the sets.
- `sets/de/python-basics/`, `sets/de/react-grundlagen/`,
  `sets/de/react-fortgeschritten/` — the lesson sets.
- `schema/` — the pinned [`learn-content-engine`](https://github.com/astrapi69/learn-content-engine)
  schema mirror; [`engine-version.txt`](schema/engine-version.txt) holds the
  pinned engine version and is the source of truth. This is what the content
  is validated against — independent of the app.
- `templates/` — starting-point lessons per domain (language / programming / knowledge).
- `scripts/validate_content.py` — the local validator.
- `scripts/generate_exercises.py` — an optional BYOK AI exercise generator.
- `generated/` — staging area for AI drafts (never shipped directly).
- `.github/workflows/` — CI that validates every push/PR against the pinned engine.
- `docs/` — [GETTING-STARTED.md](docs/GETTING-STARTED.md) and a local
  [LESSON-FORMAT.md](docs/LESSON-FORMAT.md). The **canonical, test-validated**
  format reference is the engine's
  [`docs/lesson-format.md`](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md).

## Quick start

You only need `make` and `python3`. The first `make validate` sets up a
local environment for you (no manual `pip`, no virtualenv, no Poetry):

```bash
git clone https://github.com/astrapi69/alc-programming.git
cd alc-programming

# Validate the sets. First run creates .venv and installs deps;
# later runs reuse it. Exit 0 == all sets pass.
make validate
```

Before you push, `make lint` runs the same semantic engine gate as CI
(`Engine conformance`): it installs the engine release pinned in
`schema/engine-version.txt` into `node_modules/` (gitignored; needs Node.js
and npm) and checks every lesson and manifest with the engine's rule ids
(`E-CARD-REF` & co.). `make lint-warnings` additionally prints the engine gate's warnings (`W-*`).

No `make` (e.g. Windows without WSL)? Two options: run the validator in a
virtualenv yourself —

```bash
python3 -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 scripts/validate_content.py
```

— or just commit and let the GitHub Actions CI validate (it runs the same
checks). Installing the deps globally with a bare `pip install` fails on
modern Debian/Ubuntu/macOS (PEP 668, "externally-managed-environment");
the virtualenv above is why.

Full walkthrough: [docs/GETTING-STARTED.md](docs/GETTING-STARTED.md).

## Export a set for AI review

`scripts/export_set.py` writes all lessons of ONE set into a single
YAML (or JSON) file so an AI assistant or a human can review the whole
set in one pass (syntax, correctness, consistency across lessons):

```bash
python3 scripts/export_set.py react-grundlagen
# -> exports/react-grundlagen-de-<timestamp>.yaml
python3 scripts/export_set.py react-grundlagen --format json --out /tmp/review.json
```

The slug is the set id from the root `manifest.yaml`
(`react-grundlagen-from-de`) or the folder name of the set path
(`react-grundlagen`); when the same folder name exists under several
source-language directories, `--lang` (default `de`) picks the
`sets/<lang>/` directory. Non-ASCII characters stay real UTF-8. An
unknown slug aborts with a list of the available sets.

The export is self-contained: its first field `review_instructions`
holds the complete review prompt from
[`docs/ai-review-prompt-template.md`](docs/ai-review-prompt-template.md)
(read at runtime, not copied into the script). The export file can be
handed to a review AI as-is, without manually prepending a prompt. Edit
the review instructions in that template file and keep the sibling
content repos in sync.

**Read-only snapshot, NOT a re-import format:** nothing reads the
export back. Changes flow only through the individual schema-validated
lesson JSONs under `sets/`. The `exports/` folder is gitignored.

Full usage guide and best practices (incl. the source-chapter workflow):
[`docs/export-set-usage.md`](docs/export-set-usage.md) (English) /
[`docs/export-set-usage.de.md`](docs/export-set-usage.de.md) (Deutsch).

## Export a graded quiz to PDF (school tests)

`scripts/export_quiz_pdf.py` turns a lesson that carries a graded-quiz
exercise (an `ext:*-graded-quiz`: a scored question set, points per
question, optional partial credit on multi-select, an optional
percentage pass threshold) into two print-ready PDFs:

```bash
python3 scripts/export_quiz_pdf.py path/to/graded-quiz.json --out-dir out/
# -> out/<id>-test.pdf      (question paper for students, no answers)
# -> out/<id>-loesung.pdf   (answer sheet for the teacher)
```

The test paper shows the questions with blank checkboxes / answer lines
and the points; the answer sheet shows the correct answers, the points,
a partial-credit note, and the pass threshold. This is a consumer tool -
it renders one presentation of a canonical lesson and does not invoke the
engine, so it is independent of the pinned engine version.

**Caveat (adaptive-learner-content-test#66):** graded-quiz content uses
the `ext:` extension tier, which the content gate (`make lint`) does not
yet accept (it validates core-only and refuses ext lessons). Until that
adoption lands, keep graded-quiz lessons OUTSIDE `sets/` and run the tool
on them directly (a runnable sample lives in
[`tests/fixtures/graded-quiz-sample.json`](tests/fixtures/graded-quiz-sample.json)).

## Generate exercises with AI (optional)

`scripts/generate_exercises.py` turns a topic into a full **language**
lesson with a BYOK model (Anthropic / OpenAI / Gemini) and gates every
draft through the validator before writing it into the `generated/`
staging folder. It is language-focused (target and source differ). For a
**knowledge set** like the ones in this repo (material written in the
same language it teaches, source == target), the generator is not the
right tool; hand-author from
[`templates/knowledge/`](templates/knowledge/) or
[`templates/programming/`](templates/programming/) instead.

First set your provider key. It is read from the environment (BYOK) and
never committed:

```bash
export ANTHROPIC_API_KEY="sk-..."   # or OPENAI_API_KEY / GEMINI_API_KEY (Gemini also accepts GOOGLE_API_KEY)
```

**Recommended (via make; reuses the local environment `make validate` set up):**

```bash
make generate ARGS="--topic 'Ordering food in a café' --target-lang fr --source-lang en --level A1 --set-id fr-a1"
```

**Direct (fallback; run it inside the venv from the Quick start):**

```bash
python3 scripts/generate_exercises.py \
  --topic "Ordering food in a café" \
  --target-lang fr --source-lang en --level A1 --set-id fr-a1
```

### Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--topic` | (required) | What the lesson is about. |
| `--target-lang` | (required) | The language the learner studies (BCP-47, e.g. `fr`). |
| `--source-lang` | (required) | The explanation language (BCP-47, e.g. `en`). Must differ from the target. |
| `--level` | `A1` | CEFR level. |
| `--count` | `6` | Exercises to request. The effective minimum is **5** (a smaller value is treated as 5, and the quality gate requires at least 5). |
| `--set-id` | `generated-set` | Staging subfolder under `generated/`. |
| `--provider` | `anthropic` | `anthropic` \| `openai` \| `gemini`. Or set `AL_GEN_PROVIDER`. |
| `--model` | provider default | Override the model (`claude-sonnet-4-5` / `gpt-4o` / `gemini-2.5-flash`). |
| `--retries` | `3` | Extra attempts when a draft fails validation before it is discarded. |
| `--out` | `generated` | Staging directory. |

### What happens, and what you still owe

The script pins the exact lesson-schema JSON in the prompt, parses the
model's reply, and runs it through `validate_content.py`. If validation
fails, the errors go back to the model and it retries (up to `--retries`);
a draft that never validates is discarded, not written. A valid draft
lands in `generated/<set-id>/`, never directly in `sets/`.

Two gates remain after generation, neither of them automatic:

1. **Engine semantic gate** (cloze `___` markers equal the blanks,
   `card_ids` integrity, multiselect disjointness). It runs when the
   pinned `learn-content-engine` is installed, otherwise it is deferred to
   CI. The plain validator does not cover it.
2. **Native-speaker review** for a language you do not speak natively. No
   validator catches an unnatural phrasing or a wrong romanization.
   Machine-generated, then human-verified, is the only trustworthy order.

When a draft is good, move it from `generated/` into your set under
`sets/<source>/<target>-<level>/lessons/`, register it in the set
manifest, and re-run `make validate`.

## How it stays current

The content is validated against the **pinned** engine version in
`schema/engine-version.txt` on every push and pull request (structural +
semantic + drift gates in `.github/workflows/`). A green CI means the
content is valid for every consumer of that engine release. When the
engine is bumped, it reaches this repository the same way it reaches the
rest of the chain: a deliberate pin-bump PR that the drift gate guards.

Licensed MIT (see [LICENSE](LICENSE)); the lesson content carries its own
license via each set manifest's `metadata.license`.
