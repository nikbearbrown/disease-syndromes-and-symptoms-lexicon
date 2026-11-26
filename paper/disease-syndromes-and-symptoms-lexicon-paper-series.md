# Disease, Syndromes and Symptoms Lexicon

*Rough draft, not reviewed.* A paper series modelled on *Five Papers on WordNet*. Nik Bear Brown and Humanitarians AI [TODO: confirm authorship]. Drafted 2026-11-26 with Grok Bot.

**Where it stands:** the seed list (1,079 Wikipedia pages) and replication kit are public; one independent Grok Bot edition is drafted and checked (1,077 of 1,079 pass: 932 entries, 147 out of scope, 6 duplicates, 219 ambiguous; two records still fail after their one retry). No second edition, no cross-model judging and no human review have been run. The lexicon describes clinical concepts at a high level; it gives no diagnosis or treatment advice.

## Part I. Introduction to the Disease, Syndromes and Symptoms Lexicon

### I.1 What the lexicon is for

Medical language distinguishes things that ordinary language runs together. A **disease** is a disorder with a characteristic course; a **syndrome** is a recognised cluster of features that occur together; a **symptom** is something a person experiences and reports; a **sign** is something an examiner observes. The same word can cross these lines over time, and eponymous names (*Rotch sign*, *Thevenard syndrome*) multiply the forms. This lexicon records which kind each named concept is, what it is a kind of, and what it is confused with, so that text about health can be linked to concepts without collapsing those distinctions.

### I.2 Why a WordNet-style relational lexicon

WordNet's noun paper argued that a lexical inheritance system, in which each concept inherits from its hypernym and adds a distinguishing feature, is how people store noun meanings (Miller 1990). Disease vocabularies are already hierarchical, so the inheritance idea fits. What a relational lexicon adds to a classification is the rest of the web: synonyms with conditions, look-alike names that differ, and explicit abstentions where the sources disagree about what a thing is.

### I.3 The lexical matrix, adapted

Rows are concepts, one per seed page, each fixed by a work sense; columns are names and variants with conditions. *Asperger syndrome* has the variants *Asperger's syndrome*, *Asperger's*, *AS* ("abbreviation in autism literature") and *autistic psychopathy* ("historical term"). The disease lexicon adds a fifth property to each row that the others lack: its **kind**, one of disease, syndrome, symptom or sign, or unclassified when the sources do not settle it.

### I.4 The relations

| Relation | Test the drafter must pass with the real names filled in | WordNet analogue |
|---|---|---|
| synonym | the target can replace the concept in a source excerpt without changing the concept | membership in one synset |
| hypernym | "[concept] is a kind of [target]" is true | hypernymy (@) |
| hyponym | "[target] is a kind of [concept]" is true | hyponymy (~) |
| meronym | the concept includes the target as a component by definition | part meronymy (%p) |
| holonym | the concept is a component of the target by definition | part holonymy (#p) |
| uses | the concept is characteristically associated with the target tool, material or substance | none (new) |
| requires | an explicit conceptual prerequisite supported by a source | none; compare verb entailment |
| certifies | the concept is a credential and attests to the target | none (new) |
| contrast | the target is often confused with the concept but differs from it, including look-alike names | none; replaces antonymy |

Antonyms and pertainyms are not recorded. Every relation also carries a `basis` (`source`, with pointers, or `model_knowledge`, with none) and a target that is either a seed ID or marked `proposed_new`.

**Certifies** is not used. In the Grok Bot edition the hypernym dominates (805 edges), then contrast (290), hyponym (46), synonym (15), meronym (11) and holonym (5) [counted from `drafts.jsonl` on 2026-11-26]. Contrast does here what antonymy did for WordNet's adjectives: it keeps near neighbours apart. *Acrocyanosis* is a kind of cyanosis and contrasts with *Raynaud's phenomenon*.

### I.5 Built with AI: what changes and what does not

As in the other lexicons: models draft from pinned evidence, a script checks, independent editions are compared, and people decide. Two things are specific. Kind is decided by explicit rules from the sources, and left unclassified when they disagree, so a third of the edition carries no kind yet. And the domain rule excludes any content about how disease agents are made, changed or spread.

## Part II. The vocabulary by category

The seeds come from six populated Wikipedia categories: *Syndromes* (532 direct members), *Medical signs* (321), *Infectious diseases* (149), *Symptoms* (56), *Diseases and disorders* (30) and *Infectious diseases by mode of transmission* (1). Three intended roots were empty or missing. Category is not kind: the Grok Bot edition assigned kind from Wikidata classes and the article lead, giving disease 213, syndrome 190, sign 170, symptom 19 and unclassified 340 among the 932 entries.

### II.1 Diseases

A record is a disease when Wikidata says it is an instance of disease or a type of disease, or the lead calls it a disease. Infectious diseases enter mostly here. The organising relation is the hypernym. Umbrella terms are kept as entries but flagged: *Zoonosis* is drafted as a kind of infectious disease, defined by its animal source, with a contrast to *Reverse zoonosis*, and with a `domain-rule` flag recording that no agent or transmission details are given.

### II.2 Syndromes

The largest category. A syndrome is a recognised pattern of features, and many carry eponyms, so variants and redirects are common. Thirty-nine seeds in this lexicon redirect to pages that are not seeds (*Aortic Arch Syndrome* to *Takayasu's arteritis*, *Thevenard syndrome* to *Hereditary sensory and autonomic neuropathy*); the edition flags them for mapping rather than guessing. Retired categories are kept and marked: *Asperger syndrome* is drafted as a former diagnostic category, a kind of autism spectrum disorder, flagged ambiguous because it is now subsumed.

### II.3 Symptoms

Only 19 entries are classed as symptoms, which is a finding in itself: Wikidata and Wikipedia often say "symptom or sign" without choosing, and the kind rules treat that as unclassified. Symptoms are what people report, so they are where everyday words for bodily experience meet clinical ones. A held-out kind-labelling study (Part IV) is the way to test whether models and people draw this line in the same place.

### II.4 Signs

Signs are observed, and the category is full of eponyms and bedside tests. The edition kept tests named as signs as entries but flagged them ambiguous, and placed laboratory tests out of scope. Two redirects show the care needed: *Rotch sign* redirects to a section of the list seed *List of eponymous medical signs* but names a distinct sign, so it is kept as its own concept; *Cozen's test* redirects to a section missing from the pinned revision of *Tennis elbow*, so its definition is marked model knowledge.

### II.5 What the categories pulled in

147 seeds were placed out of scope: laboratory tests, measurement methods and scales, diagnostic criteria, drugs, books, journals, laws, organisms, agents, genes and cells, organisations, hospitals, fields of study, lists, epidemiological terms, events and transmission modes, interventions, normal body processes and qualifiers. Six are duplicates by redirect, and nine records in about five pairs are possible duplicates.

## Part III. Design and implementation

### III.1 Seed list and manifest

1,079 seeds; SHA-256 `41f6251d1314ec5ceca7dbbf241e4bfbdc01e46959d626f1a2b3f03926048a68`; seed commit `31b16001`. Manifest roots: *Disease* and *Diseases* empty, *Infectious disease* missing, *Infectious diseases by type of pathogen* with subcategories only.

### III.2 Evidence bundles

English Wikipedia with each revision pinned (redirects resolved to their target with its own pinned revision, and the target section extracted when present); Wikidata with the item revision, labels, aliases and the claims P31, P279, P361, P527, P780, P1542, P828, P1199, P2176, P1995 and P737; WordNet 3.0 noun synsets. Neighbours: seeds named in the excerpts, seeds pointed to by Wikidata claims, seeds resolving to the same page, and redirect targets that are seeds; at most 25. Evidence was fetched on 2026-11-24 at about 11:06–11:08 PM EST.

### III.3 Drafting prompt and kit

Prompt gen-v2 with the domain rule: "Describe the named clinical concept at a high level. Distinguish diseases, syndromes, symptoms, signs, and non-concept pages. Do not include pathogen engineering, propagation, enhancement, dissemination, operational details, or guidance for evading detection." The repository's system prompt still speaks of "public-health terminology"; the run followed `instructions.md`. The draft schema has no `kind` field, so kind is carried in `_meta.kind`.

### III.4 Flags

The shared three, plus nine prefixes the run added: `duplicate:`, `possible-duplicate:`, `redirect-unmapped:`, `redirect-section-missing:`, `redirect-to-seed-section:`, `wikidata-error:`, `wordnet:`, `domain-rule:` and `kind-unclassified:`.

### III.5 Checking

1,077 of 1,079 pass. Of 1,079 first attempts, 23 failed (copied definitions, a malformed relation, Wikidata aliases cited inexactly, WordNet pointers while WordNet was abstained, relation types not in the schema). All 23 were retried once; 21 passed and two still fail (#2 and #12, each copying nine or more words). Under the protocol they are kept as they are and reported. 164 records carry the warning "most claims rest on model knowledge".

### III.6 Provenance

Run folder `disease-lexicon-grok-run-20261124` with the four handoff files, `DECISIONS.md` (every decision item, record by record) and `work/` (attempt log, batch sources, raw evidence). `_meta` records run mode, batch and batch size.

### III.7 The Grok Bot edition: what was done and how it deviated

Batching was approved for this run: 72 batches of 15 (the last of 14), in one session, between about 11:13 and 11:54 PM EST on 2026-11-24. The session was cut off after the final check, while RUN.md was being written; on resume nothing that had passed was redrafted, the check was rerun with the same result, and RUN.md and the judging branch were completed. Eight records were changed after drafting for consistency (for example, *APC resistance test* moved to out of scope to match other laboratory tests; *Sapronosis* moved to an umbrella entry to match *Zoonosis*); they were recompiled and re-checked but not logged as new attempts. These are disclosed deviations.

### III.8 Parallel editions and agreement

Paste-in prompt `04-disease-syndromes-and-symptoms.md`. Judging kit on `grok-agreement-method` (commit `c811edac`), adapted from the drugs kit, with a draft trap list of 42 seeds and placeholder human worked examples. A smoke test over two copies of this edition wrote 932 blinded definition requests.

### III.9 Human in the loop

People decide kind where the sources do not, scope at the borders, every redirect, and what enters the reviewed edition.

## Part IV. Evaluation (to do): what humans do after the AI comparison

### IV.1 Status

Not run. One edition exists.

### IV.2 Prerequisites on the AI side

A second blind edition, `drafters.tsv` rows, `agreement.py run`, model judges, the leak check and the panel code. See [HUMAN-EVALUATION-TODO.md](HUMAN-EVALUATION-TODO.md), Part 1.

### IV.3 Human steps in order

The steps below are the same for every lexicon and are written out once, with owners and checkboxes, in [HUMAN-EVALUATION-TODO.md](HUMAN-EVALUATION-TODO.md). They run **after** the AI side has produced its blinded, pairwise comparison of the independent editions. Every step is a human step. None has started.

| # | Human step | What it produces | Gate before the next step | Owner | Status |
|---|---|---|---|---|---|
| H1 | Settle the open decisions (IV.6): judge invitations, `drafters.tsv` rows, trap list, worked examples, weights, acceptance threshold | a committed decision record | Bear signs off | Bear | not started |
| H2 | Recruit and register human judges (`agreement.py register`) | registry rows, seeded samples | at least 2 judges for the pilot; about 10 for full scale | Bear | not started |
| H3 | Pilot: Bear and at least one other judge label the whole pilot pool; tune the rubric on the development half only; freeze the prompts (`agree-v1`) and tag the analysis plan | adjudicated pilot labels, frozen rubric | rubric frozen and tagged | Bear + 1 judge | not started |
| H4 | Human–human overlap pool: about 30% of each judge's items come from a shared pool of about 50, each item judged by at least 2 people | the **human ceiling** (Krippendorff's α, pairwise κ, before adjudication) | ceiling reported per field | human judges | not started |
| H5 | Calibrate the AI judges against people: judge–human κ per field, for the panel, for the outside-family judge alone and for each judge | acceptance per field | κ ≥ 0.6 **and** no more than 0.1 below human–human; otherwise revise the rubric on the development split only and redraw the validation sample | Bear | not started |
| H6 | Targeted review queues (IV.4): disagreements, `FAMILY_SPLIT`, low agreement, flagged records, redirects, Wikidata errors, consensus gaps | a human label for each queued item | every queued item labelled or marked `UNSURE` with a note | human judges | not started |
| H7 | Random audit of agreed items: a seeded sample of items every model agreed on | the false-agreement rate | reported with an interval | human judges | not started |
| H8 | Adjudicate: majority of human judges, ties to Bear, judges' own words kept in `notes` | one adjudicated label per reviewed item | no open ties | Bear | not started |
| H9 | Verify claims (correctness, not agreement): for every claim kept, a reviewer opens the cited source and marks `supports`, `contradicts` or `unsure`; claims with only `model_knowledge` basis are sourced or withheld | per-claim decisions | no kept claim without a named check | reviewers | not started |
| H10 | Domain-safety review against the lexicon's rule (IV.4) | a pass or a list of removals | zero open safety items | Bear or a named domain reviewer | not started |
| H11 | Scope, duplicate and redirect decisions, with a crosswalk to the original seed IDs | decision list and crosswalk | every flagged seed decided | Bear | not started |
| H12 | Accept or reject merged entries into the reviewed edition (`lexicon/entries.jsonl`), with per-claim decisions, contributing run IDs and a named reviewer | the first reviewed entries | each accepted entry has a named reviewer and no unresolved contradiction | Bear | not started |
| H13 | Held-out task and coverage evaluations (IV.5) | task scores with intervals | analysis plan fixed before annotation | Bear + raters | not started |
| H14 | Write up: human ceiling, judge–human agreement, false-agreement rate, safety outcome, accepted-entry counts | the evaluation section of this paper | Bear approves | Bear | not started |

Agreement between models is not evidence that an entry is right. Steps H9 to H12 exist because two models can agree on the same mistake.

### IV.4 What humans review in this lexicon

Editions available today: **one**, the Grok Bot edition (1,079 records, 932 entries; `check.py` 1,077 of 1,079). The comparison needs a second blind edition (paste-in prompt `04-disease-syndromes-and-symptoms.md`). The run's `DECISIONS.md` already lists every item below record by record.

| Queue | Source | Size in the Grok edition | What the human decides |
|---|---|---:|---|
| Kind unclassified | `kind-unclassified:` | 340 (295 with no source classing them, 45 where sources conflict) | disease, syndrome, symptom, sign, or leave unclassified |
| Ambiguous | `ambiguous:` | 219 | in scope or not; e.g. bedside tests named as signs, vital signs, umbrella terms, disputed or popular labels, obsolete diagnoses, veterinary diseases |
| Out of scope | `out-of-scope:` | 147 | confirm (lab tests, scales, criteria, drugs, organisms, genes, organisations, lists, interventions, normal processes) |
| Redirects to pages that are not seeds | `redirect-unmapped:` | 39 | new concept, map, or abstain |
| Redirect sections missing at the pinned revision | `redirect-section-missing:` | 4 | accept the model-knowledge definition or re-source it |
| Redirects to a section of a seed, kept distinct | `redirect-to-seed-section:` | 2 | confirm they are separate concepts |
| Duplicates and possible duplicates | `duplicate:`, `possible-duplicate:` | 6 and 9 | map or keep |
| Wikidata errors | `wikidata-error:` | 241 records [counted from `drafts.jsonl` flags on 2026-11-26] | confirm the error and that it was not used |
| Failing records | `report.jsonl` | 2 (#2 Abadie's sign of exophthalmic goiter, #12 Acholia: both copy nine or more words after their one retry) | accept with an exception, or redraft under a new attempt |
| Post-hoc consistency edits | RUN.md, deviation 3 | 8 records (#14, #306, #335, #357, #441, #444, #705, #839) | confirm each change; they were recompiled and re-checked but not logged as new attempts |
| Thin evidence | warning "most claims rest on model knowledge" | 164 | entries go first in H9 |

**Kind as a human task.** The kind (disease, syndrome, symptom, sign) is this lexicon's main organising decision, and the Grok edition left a third of the records unclassified rather than guess. Humans label kind on the unclassified queue and on a random sample of classified records, so that the edition's kind rules (RUN.md) are tested, not assumed.

**Domain-safety review (H10).** The rule: describe the named clinical concept at a high level; no pathogen engineering, propagation, enhancement, dissemination or operational details; no guidance for evading detection; no diagnosis or treatment advice for a person. The reviewer reads every definition and relation, the 86 records carrying a `domain-rule` flag first [counted from flags], and the infectious-disease strata (Infectious diseases; by mode of transmission) in full. Pass criterion: no transmission mechanics beyond naming the route class, no agent details, and nothing a reader could take as a diagnosis or treatment instruction.

### IV.5 Held-out task and coverage evaluations

- **Kind classification.** Human kind labels on a seeded, stratified sample (by root category), against each edition's kind. Measures whether models and people draw the disease–syndrome–symptom–sign lines in the same place. Status: not designed.
- **Coverage.** Map a sample to ICD-11, MeSH (Diseases; Pathological Conditions, Signs and Symptoms), and the Human Phenotype Ontology for signs and symptoms. SNOMED CT clinical findings if licensed [TODO: licence]. Status: not designed.
- **Mention linking.** Public descriptive text only, never records about a person [TODO: choose the corpus].

### IV.6 Open decisions

- The seven "Decisions for Bear" in `AGREEMENT-METHOD.md` §12 on `grok-agreement-method` (c811edac), including the draft trap list of 42 seeds and the placeholder human worked examples.
- The two failing records and the eight post-hoc edits (IV.4).
- The scope rules (lab tests out of scope; umbrella terms kept as entries) and the kind rules in RUN.md.
- The extra flag prefixes the run added beyond `instructions.md`: `duplicate:`, `possible-duplicate:`, `redirect-unmapped:`, `redirect-section-missing:`, `redirect-to-seed-section:`, `wikidata-error:`, `wordnet:`, `domain-rule:`, `kind-unclassified:`. Adopt them for all editions or map them.
- A conflict in the repository: the system prompt speaks of "public-health terminology", while `instructions.md` asks for the clinical concept. The run followed `instructions.md`.
- The draft schema has no `kind` field; kind is carried in `_meta.kind`. Decide whether the schema should gain one.
- Root categories that were empty or missing (`Category:Disease`, `Category:Diseases`, `Category:Infectious disease`).
- Who drafts the second edition.

### IV.7 Resources, owners and status

About 10 human judges at about 100 items each; additional kind labelling for the 340 unclassified records [TODO: raters and hours]; a clinically trained domain-safety reviewer for H10. Tools: `agreement.py register`, `validate`, `stats`. Owner: Bear unless delegated. Status: not started.

## Part V. Limitations

Kind rules rest on Wikidata classes and Wikipedia leads, both of which are inconsistent. A third of entries are unclassified. Two records fail the copy check. The edition was batched and had post-hoc edits.

## Appendix A. File formats

**Seeds** (`data/seeds.tsv`): `concept_id`, `page_id`, `preferred_name`, `source_url`, `direct_categories`. **Kind** is carried in each draft's `_meta.kind` and `_meta.kind_pointers`.

**Evidence bundle** (`bundles.jsonl`, one JSON object per seed, exactly seven top-level fields):

| Field | Content |
|---|---|
| `concept_id` | the seed ID, unchanged |
| `concept` | `id`, `preferred_name`, `kind` and `broad_class` (`unclassified` until supported), `variants` and `relations` (start empty) |
| `neighbors` | candidate relation targets, taken only from the seed list, each `{id, name}` |
| `examples` | optional public terminology excerpts `{id, source URL, text}` |
| `wikipedia` | up to three `{title, revision_id, text}`; the revision is pinned |
| `wikidata` | candidate items `{qid, label, aliases, claims, revision_id}` and ancestors marked `ancestor_of` |
| `wordnet` | matching senses `{synset, lemmas, gloss, relations}` |

**Draft** (`drafts.jsonl`, one JSON object per seed, prompt gen-v2):

| Field | Content |
|---|---|
| `concept_id` | the seed ID |
| `work_sense` | one sentence fixing the sense every later decision is about (the name is kept from the first lexicon for schema compatibility) |
| `links.{wikipedia,wikidata,wordnet}` | `{choice, reason}`; `choice` is a revision ID, QID or synset ID, or `null` to abstain |
| `definition` | `{text, basis, pointers}`; one to three sentences, never more than eight consecutive words from a source |
| `variants[]` | `{text, condition, basis, pointers}`; `condition` says when the form names the concept |
| `relations[]` | `{type, target_label, target_id, proposed_new, basis, pointers, note}` |
| `flags[]` | strings, each a prefix and a reason (Appendix B) |
| `_meta` | added after drafting: model and version (or `unknown`), run mode, attempt count, and for retries the errors that triggered them |

**Pointer forms:** `wd:QID#PID=VALUE_QID`, `wd:QID#alias=TEXT`, `wn:SYNSET#lemma=TEXT`, `wn:SYNSET#RELATION=TARGET`, `wp:REVISION_ID#quote=TEXT` (at most 20 words, copied exactly), `ex:EXAMPLE_ID`.

**Check report** (`report.jsonl`): one line per seed, `{concept_id, status: pass|fail, errors[], warnings[]}`.

**RUN.md:** dates, seed commit and hash, model and settings, tools, evidence sources, deviations, coverage totals, retries and unresolved failures.

## Appendix B. Flags

| Prefix | Meaning |
|---|---|
| `out-of-scope:` | no usable clinical concept |
| `ambiguous:` | unresolved evidence, scope or sense |
| `duplicate:` / `possible-duplicate:` | redirect to another seed / two seeds may be one concept |
| `redirect-unmapped:` | redirects to a page that is not a seed |
| `redirect-section-missing:` | the target section is absent from the pinned revision |
| `redirect-to-seed-section:` | redirects to a section of a seed but names a distinct concept |
| `wikidata-error:` | a Wikidata class or alias judged wrong, not used as evidence |
| `wordnet:` | a WordNet sense that does not match usage |
| `domain-rule:` | content left out under the domain rule |
| `kind-unclassified:` | sources do not settle the kind, or disagree |

## Appendix C. Scripts

`render.py`, `check.py`, `verify_drafts.py`, and `agreement.py` on `grok-agreement-method`. The run's own tools (`fetch.py`, `build.py`, `compile.py`) are in the private run folder.

## References

- Miller, G. A., Beckwith, R., Fellbaum, C., Gross, D., and Miller, K. J. 1990. Introduction to WordNet: An on-line lexical database. *International Journal of Lexicography* 3(4): 235–244. Revised in *Five Papers on WordNet*, CSL Report 43, Princeton University, 1990, revised 1993.
- Miller, G. A. 1990. Nouns in WordNet: A lexical inheritance system. *International Journal of Lexicography* 3(4): 245–264.
- Gross, D., and Miller, K. J. 1990. Adjectives in WordNet. *International Journal of Lexicography* 3(4): 265–277. Revised as Fellbaum, Gross and Miller in *Five Papers on WordNet*, 1993.
- Fellbaum, C. 1990. English verbs as a semantic net. *International Journal of Lexicography* 3(4): 278–301.
- Beckwith, R., Miller, G. A., and Tengi, R. 1993. Design and implementation of the WordNet lexical database and searching software. In *Five Papers on WordNet*.
- Miller, G. A. 1995. WordNet: A lexical database for English. *Communications of the ACM* 38(11): 39–41.
- Fellbaum, C., ed. 1998. *WordNet: An Electronic Lexical Database*. MIT Press.
- Vrandečić, D., and Krötzsch, M. 2014. Wikidata: A free collaborative knowledgebase. *Communications of the ACM* 57(10): 78–85.
- Krippendorff, K. 2018. *Content Analysis: An Introduction to Its Methodology*, 4th ed. SAGE.
- Fleiss, J. L. 1971. Measuring nominal scale agreement among many raters. *Psychological Bulletin* 76(5): 378–382.
- Shared methods paper: *Building WordNet-style lexica with AI: process and provenance* (`building-wordnet-style-lexica-with-ai.md` in this folder).
- ICD-11, MeSH, the Human Phenotype Ontology and SNOMED CT are named in IV.5 as candidate reference vocabularies [TODO: add citations when the coverage study is designed].
