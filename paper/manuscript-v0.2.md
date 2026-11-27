# A Disease, Syndrome, and Symptom Lexicon for Auditable Text Review

Humanitarians AI | Revised rough methods manuscript v0.2 | November 2026

## Abstract

Formal names, lay phrases and abbreviations can refer to the same concept, but can also refer to different things depending on context. We propose a reproducible way to build a reviewer-maintained vocabulary from independent model editions and verify the evidence supporting accepted entries. We specify three evaluations: interpretation of public language, literature discovery, and source-linked extraction from fictional reports. No comparative or clinical results are reported.

## Construction and review

The [frozen seed manifest](../data/README.md) contains 1,079 English Wikipedia article pages, not 1,079 validated concepts. Keep page provenance and record compound, duplicate, unclear and out-of-scope seeds rather than forcing each into one concept. Use the [replication kit](../replication/README.md) for separate blinded model editions. Freeze each edition before comparison. Report structural validity, comparable entries, agreement on class and aliases, and source-review outcomes with separate denominators. A model consensus is not verification. Record independent reviewer judgments before adjudication and exclude unresolved aliases from active releases. Compare reviewed concepts to the National Library of Medicine’s [MeSH](https://www.nlm.nih.gov/mesh/meshhome.html) where applicable; do not assume equivalence.

## Evaluation

| Question | Comparison and outcome |
|---|---|
| Do aliases improve interpretation of public language? | On the same held-out fictional organizational documents, compare a fixed literal list with reviewed aliases. Annotate spans and distinct documents. Count correct senses, missed target concepts and new wrong-sense matches separately by concept class. |
| Does the lexicon improve literature discovery? | Compare a fixed title/abstract plus applicable MeSH baseline with reviewed alias expansion in the same indexed snapshot. Blind-label pooled paper–topic pairs. Report precision at a fixed shortlist size and additional relevant papers within the judged pool, not corpus-wide recall. |
| Does the lexicon help draft report fields? | Hold the parser and extractor constant; vary the vocabulary on fictional reports. Count supporting evidence spans, correct fields, missed fields, unsupported fields and abstentions. A later approved study could measure time and corrections per document. |

Separate development and test by document template and topic family as appropriate. Lock match rules before testing and adjudicate labels without seeing which method produced a hit. For uncertainty, account for shared documents or search topics rather than treating every match as independent. Synthetic trap frequency cannot estimate real-world precision.

## Reproducibility and release decisions

The [source manifest](../data/source-manifest.json) records the frozen seed hash. A replication record should retain the manifest hash, prompt and model versions, counts of all valid, invalid and abstained entries, and the separate decisions of the evidence reviewers. Use one output per seed even when no defensible entry can be drafted. Class agreement is calculated only among comparable class labels and accompanied by the count excluded for missing or unclear labels. Separately report how often reviewers agree that a cited source supports a claim. Do not classify model consensus as support.

For the extraction test, label one record template before drafting data, including which fields must be empty and where each nonempty value is supported. If a response gives a correct-looking value with no supporting span, record that separately from a supported extraction. Reserve a held-out set of report templates and keep the relevant units visible in the figure.

**Figure 2 design:** Paired points for correct supported fields and missed fields per 100 eligible fields, with unsupported fills per 100 total opportunities shown in a separate panel. Label the raw denominators and cluster by document when estimating uncertainty. This is a figure specification, not a rendering or a result.

[NEEDS: finalized report schema and label rubric, named baseline version, held-out sample size and verified terminology mappings.]

## Agentic workflows

[Figure 1](agentic-workflows.md) shows Social Media Agent for finding vocabulary ambiguities and Research Ledger for explaining why a paper appears in a reader’s shortlist. Each independently consumes the same reviewed lexicon. Only a reviewed release, not source records or inferred labels, transfers between tasks. Neither workflow replaces document-level validation.

## Status and limitations

The seed manifest and replication kit exist. A validated lexicon release, a labeled benchmark and performance results are not claimed. Wikipedia coverage and English-language bias should be reported. Future clinical data use would require separate approval and infrastructure. This is a research method, not a diagnostic or treatment system.
