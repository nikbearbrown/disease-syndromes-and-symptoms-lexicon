# Disease, Syndromes and Symptoms Lexicon: independent Grok Bot edition (private run)

Run directory: `/workspace/disease-lexicon-grok-run-20261124` (private, unpushed).
Files saved together: `bundles.jsonl`, `drafts.jsonl`, `report.jsonl`, `RUN.md`, plus `DECISIONS.md` (full per-record lists of every decision item) and `work/` (attempt log, batch DSL sources, raw evidence, tools in `tools/`).

## Dates (America/New_York, EST)
- Evidence fetched: 2026-11-24, about 11:06–11:08 PM EST (box clock logs UTC: 2026-11-25 04:06–04:08 UTC).
- Bundles built: 11:11 PM EST. Drafting: batch 1 logged 11:13 PM EST, batch 72 logged 11:54 PM EST (2026-11-24).
- check.py over the complete run: 2026-11-24 11:54 PM EST, re-run after the interruption on resume (same result).
- **Interruption:** the session was cut off after the final check.py run, while RUN.md was being written and before the judging branch was made. On resume nothing that had passed was redrafted; the two failing records had already used their single retry, so none was given; check.py was re-run, then RUN.md, the backup and the judging branch were completed.

## Seed frame
- Repo `nikbearbrown/disease-syndromes-and-symptoms-lexicon`, seed commit `31b16001` (31b1600172731e9b8a662df730be4aaa27bd9ece), fresh checkout at `/workspace/disease-lexicon-checkout` (detached HEAD at the seed commit).
- `data/seeds.tsv`: 1,079 seeds; sha256 `41f6251d1314ec5ceca7dbbf241e4bfbdc01e46959d626f1a2b3f03926048a68`, verified against `data/source-manifest.json` before drafting. seeds.tsv and the manifest were not changed.
- Manifest root categories: `Category:Disease` empty, `Category:Diseases` empty, `Category:Infectious disease` missing. `Category:Infectious diseases by type of pathogen` exists but has no article members (6 subcategories only). Found roots used as strata: Diseases and disorders, Infectious diseases, Infectious diseases by mode of transmission, Symptoms, Syndromes, Medical signs.

## Model and settings
- Drafter: Grok Bot (executor agent). Model string: **unknown** (not exposed to the agent; not guessed). Temperature and sampling settings: not exposed.
- Run mode: batched, **15 seeds per batch** throughout (72 batches; the last holds 14), all in one session. Recorded in every record's `_meta.run_mode`, `_meta.batch`, `_meta.batch_size`.
- Blind: no other run, edition, reviewer vote or model entry was read; no other agent drafted or judged. In `/workspace/drugs-lexicon-checkout` only the judging-kit files on branch `grok-agreement-method` (ab14590) were read, for step 4.

## Tools
- Python 3.13 scripts in `tools/`: `fetch.py` (MediaWiki and Wikidata APIs), `build.py` (bundles and drafting views), `view.py`/`go.sh` (per-batch views, save after every batch, tgz backup every 5 batches), `compile.py` (turns the agent's per-batch drafting notes in `work/dsl/bNNN.txt` into draft JSON, runs the repo's checks per record and logs attempts to `work/attempts.jsonl`).
- Self-review step: before a batch was logged, `compile.py --dry` ran the repo's own 9-word copy test on the definitions and the agent reworded any hit. This is a pre-check, not a retry; only logged compiles count as attempts.
- WordNet 3.0 via NLTK (installed in an existing local tool virtualenv, `/workspace/venv-clinlex`, used only as a library).
- `replication/scripts/check.py` from the seed commit, unchanged.

## Evidence sources
- English Wikipedia via the API: each seed's page revision pinned (`revision_id` in bundles); redirect seeds resolved to their target page with its own pinned revision, and the target section extracted when present.
- Wikidata via the API: the item linked from the page (`wikibase_item`), with `lastrevid`, labels, aliases and claims P31, P279, P361, P527, P780, P1542, P828, P1199, P2176, P1995, P737.
- WordNet 3.0 noun synsets matching the seed title.
- Neighbours: only seeds, found by (a) another seed's title appearing in this seed's excerpts, (b) a Wikidata claim pointing to a seed's page, (c) seeds resolving to the same page, (d) the redirect target being a seed; max 25.

## Coverage totals
- Records: 1,079 drafts, 1,079 bundles, one per concept_id, no seed dropped.
- Entries 932; out of scope 147. Duplicates 6. Possible-duplicate flags 9 (5 pairs or near pairs). Ambiguous 219.
- `kind` on entries: disease 213, syndrome 190, sign 170, symptom 19, unclassified 340 (295 with no source classing them, 45 where sources conflict).
- check.py: **1,077 / 1,079 pass**. Warnings: 164 × "most claims rest on model knowledge".
- Attempts: 1,079 first attempts; 23 first-attempt failures; 23 retries; 21 passed on retry, 2 still fail.

## Failures and retries (why each first attempt failed)
- Copying 9+ consecutive words in the definition: #2 Abadie's sign of exophthalmic goiter, #13 Acrocyanosis, #42 Ascending cholangitis, #44 Asperger syndrome, #237 Elschnig spots.
- A relation object failed check.py's claim format ("invalid claim"): #12 Acholia.
- Variant cited a Wikidata alias that does not exist verbatim (spelling or wording mismatch): #25, #391, #445, #463, #809, #838, #856, #929, #965, #986, #1063.
- WordNet lemma pointers while WordNet was abstained: #478 Lethargy.
- Relation types not in the schema ("associated", "similar"): #752, #758, #760, #762, #763.
- **Still failing after the retry:** #2 (definition copies "appearance it is named for Jean-Marie-Charles Abadie") and #12 (retry definition copies "colour; it is a sign of reduced conjugated bilirubin"). Kept as is.

## Deviations from the protocol
1. Batching (approved) instead of fresh context per seed: 15 per batch in one session.
2. Interruption before RUN.md and the judging branch (see Dates); resumed without redrafting.
3. Post-hoc consistency edits without logging new attempts (all recompiled and re-checked): #357 relation changed to meronym and flag reworded; #705 removed a self-contradictory wikidata-error flag; #14 APC resistance test changed from entry to out of scope (lab tests are out of scope everywhere else); #839 Sapronosis changed from out of scope to an umbrella entry, to match Zoonosis and Tropical disease; #306, #335, #441, #444 dropped or changed a hypernym that the record's own wikidata-error flag said was wrong.
4. Self-review pre-check with the repo's copy test before logging each batch (see Tools).
5. Extra flag prefixes beyond instructions.md: `duplicate:`, `possible-duplicate:`, `redirect-unmapped:`, `redirect-section-missing:`, `redirect-to-seed-section:`, `wikidata-error:`, `wordnet:`, `domain-rule:`, `kind-unclassified:`.

## Conflicts between the brief and the repo (repo wins)
- The draft schema has no `kind` field. Kind is carried in the bundle's `concept.kind` and in each draft's `_meta.kind` / `_meta.kind_pointers`; unclassified records carry a `kind-unclassified:` flag.
- instructions.md asks for fresh context per seed; the brief approves batching. Batching was used and recorded.
- The repo's system prompt mentions "public-health terminology"; drafts describe the clinical concept as the brief and instructions.md domain line say.

## Kind rules used
- sign: Wikidata P31 clinical sign (Q1441305) or radiologic sign (Q2202754), or the article lead calls it a sign.
- disease: P31 disease (Q12136) or type of disease (Q112193867), or the lead calls it a disease.
- syndrome: P31/P279 syndrome (Q179630), or the lead calls it a syndrome.
- symptom: P31 symptom (Q169872 / Q30897648), or the lead calls it a symptom.
- "symptom or sign" alone, or sources that disagree: unclassified, flagged.

## Scope rules used
- Out of scope: lab tests, measurement methods, calculated measures and scales, diagnostic criteria, drugs, books, journals, laws, organisms, agents, genes and cells, organisations, hospitals, fields of study, lists and outlines, epidemiological terms, events and transmission modes, interventions, normal body processes and behaviours, descriptors and qualifiers.
- Entries flagged ambiguous: bedside examination tests named as signs, vital signs and measured functions, umbrella terms, disputed or popular labels, lab findings, obsolete diagnoses, disambiguation targets, veterinary diseases.

## Redirects
- 39 seeds redirect to non-seed pages: flagged `redirect-unmapped`, mapping left to the maintainer (list in DECISIONS.md).
- 4 redirect to a section missing from the pinned revision: flagged, definition marked model knowledge.
- 6 redirect to another seed: flagged duplicate. 2 redirect to a section of a seed but name a distinct concept: kept as entries, flagged.

## Backups
- `/cursor/stores/store-b70b09de-a0d7-4d1b-a3f4-5cf53c567708/disease-lexicon/disease-lexicon-grok-run-20261124.tgz`, refreshed every 5 batches and at the end.

## Judging branch
- `grok-agreement-method` pushed to origin at commit c811edac (author and committer nikbearbrown <610338+nikbearbrown@users.noreply.github.com>), branched from the seed commit 31b16001. It holds the agreement kit only, adapted from the drugs lexicon kit (ab14590) by `tools/port_kit.py`: AGREEMENT-METHOD.md, judging/, scripts/agreement.py and 4 added lines in replication/README.md. No drafts, bundles or source text. The trap list (TRAP_IDS, 42 seeds) is marked as a draft for review; the human worked examples are marked placeholders. main was not touched; no PR.
- Smoke test: `agreement.py run` over two copies of this run's drafts in /tmp wrote 932 blinded P2 requests; the /tmp output was deleted.
