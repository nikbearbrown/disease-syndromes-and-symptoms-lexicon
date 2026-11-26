# Parallel editions

Independent, machine-drafted editions of this lexicon, kept here as parallel evaluations so they can be compared side by side. Each subfolder is one model's edition.

- **Unreviewed.** Every record is a machine draft. None has been checked by a person, and none is part of the reviewed lexicon in [`lexicon/`](../lexicon/README.md).
- **Not for drafters.** If you are drafting an independent edition with the [replication kit](../replication/README.md), do not open this folder until your edition is frozen. The kit's blindness rule covers every edition here.
- **Unedited copies.** The files inside an edition folder are copied unchanged from that model's private run folder. Nothing was hand-edited after the edition's final `check.py` run. Paths inside `RUN.md` and the tools refer to the drafter's own machine.
- Wikipedia text in the bundles is CC BY-SA 4.0, with the exact revision id pinned per record; Wikidata is CC0; WordNet 3.0 is under the WordNet licence.

## Editions

| Folder | Model as recorded | Run mode | Date | Seed commit | `data/seeds.tsv` sha256 | Records | `check.py` |
|---|---|---|---|---|---|---|---|
| [`grok-bot/`](grok-bot/) | Grok Bot (exact version: unknown, not exposed to the drafter) | Batched: 72 batches of 15 seeds (the last holds 14) in one session, not a fresh context per seed. Approved by the project owner and disclosed in `RUN.md` and every `_meta.run_mode`. | 2026-11-24 (EST) | `31b1600172731e9b8a662df730be4aaa27bd9ece` | `41f6251d1314ec5ceca7dbbf241e4bfbdc01e46959d626f1a2b3f03926048a68` | 1,079 / 1,079 seeds | 1,077 pass, **2 fail** (#2 and #12: definitions still copy source wording after their single retry; kept as is, per the kit) |

## `grok-bot/`: files

| File | What it is |
|---|---|
| `RUN.md` | Model, seed commit and hash, sources, method, failures and retries |
| `DECISIONS.md` | Every decision item for review, per record: redirects, duplicates, out of scope, ambiguous, unclassified kinds, Wikidata errors, WordNet notes, detail left out under the domain rule |
| `drafts.jsonl` | One draft per seed, each with `_meta` |
| `report.jsonl` | `check.py` output per seed |
| `bundles.jsonl` | Evidence bundle per seed: pinned Wikipedia revision, Wikidata, WordNet 3.0, neighbors |
| `tools/` | Fetch, build, view and compile scripts |

## Left out of `grok-bot/`, and why

- `work/` (attempt log, per-batch drafting sources, views, raw API responses). This repository's `.gitignore` excludes `work/`, and the records it produced are in `drafts.jsonl`.
- No rendered entries file exists for this edition.
- No keys, secrets or judging anonymisation files are included.

More editions from other models can be added as sibling folders, for example `editions/<model>/`, with a row in the table above.
