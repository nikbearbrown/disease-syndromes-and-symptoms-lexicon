import re,sys
from pathlib import Path
R=Path('.')
SYS_OLD="""You compare entries from a descriptive dictionary of drugs and recreational drug use (substances, substance
classes, practices and patterns of use, substance-related disorders, harm reduction and other public-health
terms) as named in Wikipedia."""
SYS_NEW="""You compare entries from a descriptive dictionary of diseases, syndromes, symptoms and medical signs
(including infectious diseases and other public-health terms) as named in Wikipedia."""
SYS2_OLD="""The dictionary describes
substances, substance classes and public-health terminology; it never gives synthesis, procurement, dosing or
concealment guidance, so do not add any, and do not judge whether a drug, practice or policy is good or bad.
Never infer demographics (who uses a drug) from individual mentions, and never write about an identifiable
person's drug use. Return only the JSON object asked for."""
SYS2_NEW="""The dictionary describes
each named clinical concept at a high level; it never gives pathogen engineering, propagation, enhancement,
dissemination or operational details, or guidance for evading detection, so do not add any, and give no
diagnosis or treatment advice. Never write about an identifiable person's health or medical records.
Return only the JSON object asked for."""
P1_OLD="""drug, public-health or encyclopaedic usage (same referent), even if one is broader or narrower. Different
referents (for example a substance versus the practice of using it, a drug versus the disorder it causes, or a
street name versus an unrelated everyday word) go in different groups."""
P1_NEW="""clinical, public-health or encyclopaedic usage (same referent), even if one is broader or narrower. Different
referents (for example a sign versus the disease it points to, a symptom versus a syndrome of the same name, or
two eponymous signs or syndromes sharing a person's name) go in different groups."""
P2_OLD="what it consists of or acts on, its drug class or main effects, where or by whom a name is used)."
P2_NEW="its cause, its main features or affected body system, what it indicates, where or by whom a name is used)."
P3_OLD="""{Variants: a variant matches only if, in drug, public-health or
encyclopaedic usage, it would name this same concept.} {Targets: ignore the relation type; group by what the target is.}
Do not group a thing with a broader or narrower thing (crack cocaine is not cocaine; a synthetic cannabinoid is not
cannabis)."""
P3_NEW="""{Variants: a variant matches only if, in clinical, public-health or
encyclopaedic usage, it would name this same concept.} {Targets: ignore the relation type; group by what the target is.}
Do not group a thing with a broader or narrower thing (upper respiratory tract infection is not respiratory tract
infection; Murphy's triad is not Murphy's sign)."""
COMMON=[(SYS_OLD,SYS_NEW),(SYS2_OLD,SYS2_NEW),(P1_OLD,P1_NEW),(P2_OLD,P2_NEW),(P3_OLD,P3_NEW)]
ORIGIN_OLD="adapted from the Clinical Treatments and Procedures Lexicon's agreement kit (`nikbearbrown/clinical-treatments-and-procedures-lexicon`, branch `grok-agreement-method`, commit 51774fbd), itself ported from the Irreducibly Human Work Lexicon's kit (78f889a2), and its clinical rules were replaced by this repository's domain rule."
ORIGIN_NEW="adapted from the Drugs and Recreational Drug Use Lexicon's agreement kit (`nikbearbrown/drugs-and-recreational-drug-use-lexicon`, branch `grok-agreement-method`, commit ab14590), itself adapted from the Clinical Treatments and Procedures Lexicon kit (51774fbd) and the Irreducibly Human Work Lexicon kit (78f889a2), and its drug rules were replaced by this repository's domain rule."
FRAME="1,079 seeds"
S={}
S['AGREEMENT-METHOD.md']=[
("of the Drugs and Recreational Drug Use Lexicon","of the Disease, Syndromes and Symptoms Lexicon"),
("from the Clinical Treatments and Procedures Lexicon agreement method (`nikbearbrown/clinical-treatments-and-procedures-lexicon`, branch `grok-agreement-method`, commit 51774fbd; itself ported from the Irreducibly Human Work Lexicon kit, 78f889a2). The schema (gen-v2) and the method are unchanged; the clinical content rules are replaced",
 "from the Drugs and Recreational Drug Use Lexicon agreement method (`nikbearbrown/drugs-and-recreational-drug-use-lexicon`, branch `grok-agreement-method`, commit ab14590; itself adapted from the Clinical Treatments and Procedures Lexicon kit, 51774fbd, and the Irreducibly Human Work Lexicon kit, 78f889a2). The schema (gen-v2) and the method are unchanged; the drug content rules are replaced"),
(re.compile(r"\*\*Domain rule \(binds every drafter, judge and operator\)\.\*\*.*"),
 "**Domain rule (binds every drafter, judge and operator).** From [instructions.md](instructions.md) and [prompts/system.txt](prompts/system.txt): describe the named clinical concept at a high level; distinguish diseases, syndromes, symptoms, signs and non-concept pages; do not include pathogen engineering, propagation, enhancement, dissemination, operational details or guidance for evading detection; use public sources only and include no private or identifiable records. Judges compare meanings without adding any such detail and without giving diagnosis or treatment advice. No request, packet, result, note or rationale may contain an identifiable person's health information; an item that appears to is labelled `UNSURE` with the note \"possible identifiable health information\" and reported to the operator."),
(re.compile(r"\*\*Concept frame\.\*\* The 352 seeds .*?contribute no seeds\."),
 "**Concept frame.** The 1,079 seeds of [../data/seeds.tsv](../data/seeds.tsv) (seed commit 31b16001, sha256 `41f6251d1314ec5ceca7dbbf241e4bfbdc01e46959d626f1a2b3f03926048a68`, see [../data/source-manifest.json](../data/source-manifest.json)): direct members of Category:Diseases and disorders, Category:Infectious diseases, Category:Infectious diseases by mode of transmission, Category:Symptoms, Category:Syndromes and Category:Medical signs on English Wikipedia. Three manifest roots contribute no seeds: Category:Disease and Category:Diseases were empty and Category:Infectious disease was missing at retrieval; Category:Infectious diseases by type of pathogen has subcategories but no direct article members."),
("here it states the sense in drug and public-health usage","here it states the sense in clinical and public-health usage"),
("(drugs, psychoactive-drugs, drug-culture, substance-abuse, substance-related-disorders, or multiple)","(diseases-and-disorders, infectious-diseases, infectious-diseases-by-mode-of-transmission, symptoms, syndromes, medical-signs, or multiple)"),
("reworded for drugs and recreational drug use,","reworded for diseases, syndromes, symptoms and signs,"),
("such as \"(drug)\", \"(drugs)\" or \"(smoking)\" instead of","such as \"(disease)\", \"(medicine)\", \"(medical sign)\" or \"(syndrome)\" instead of"),
("(*Kush* as a synthetic street drug versus cannabis strains named kush, for example)","(*Abadie's sign* of tabes dorsalis versus Abadie's sign of exophthalmic goiter, for example)"),
("a trailing \"(drug)\" style qualifier dropped","a trailing \"(disease)\" style qualifier dropped"),
("\"A says: a speedball is a kind of polysubstance use. B says: a speedball routinely includes cocaine as a component.\"",
 "\"A says: an upper respiratory tract infection is a kind of respiratory tract infection. B says: an upper respiratory tract infection is a part of respiratory tract infection.\""),
("Background in pharmacology or public health is not required","Background in medicine or public health is not required"),
]
S['judging/AI-JUDGE-INSTRUCTIONS.md']=[
("of the Drugs and Recreational Drug Use Lexicon","of the Disease, Syndromes and Symptoms Lexicon"),
("(descriptive only; no harmful guidance; no demographic inference)","(descriptive only; no harmful guidance; no personal health information)"),
(re.compile(r"\): describe substances, substance classes and public-health terminology; qualify regional or ambiguous aliases; give no synthesis.*"),
 "): describe the named clinical concept at a high level; distinguish diseases, syndromes, symptoms, signs and non-concept pages; give no pathogen engineering, propagation, enhancement, dissemination or operational details and no guidance for evading detection; use public sources only, with no private or identifiable records."),
(re.compile(r"- \*\*Descriptive only\.\*\* Judge only.*"),
 "- **Descriptive only.** Judge only whether two entries mean the same thing. Never add, suggest or correct how a pathogen could be engineered, propagated, enhanced or disseminated, or how detection could be evaded, and do not judge whether a treatment or policy is good or bad. An entry that reports a source's evidence or historical status (\"no longer used as a diagnosis\") is compared as a claim like any other."),
(re.compile(r"- \*\*Regional and ambiguous names\.\*\*.*"),
 "- **Eponyms and ambiguous names.** Entries qualify eponymous, historical or ambiguous names (for example \"historical\", or \"in hyperthyroidism\" for one of two signs that share a person's name). Treat that condition as part of the variant's meaning when you compare variants (P5)."),
(re.compile(r"- \*\*No demographic inference, no personal details\.\*\*.*"),
 "- **No personal health information.** Never paste, request or write details of an identifiable person's health, symptoms or medical records, including your own, a judge's or someone you know, in a result, note or rationale. If an item seems to contain such details, label it `UNSURE`, write `\"notes\": \"possible identifiable health information\"`, and tell the operator. Do not repeat it."),
(re.compile(r"- \*\*No advice\.\*\*.*"),
 "- **No advice.** If a person in a session asks for medical, diagnostic or treatment advice, do not give it inside the study; say that the study only compares dictionary meanings."),
("(for example *ecstasy* as the drug MDMA against *ecstasy* as an emotional state; or a substance against the disorder it causes)",
 "(for example *Murphy's sign* of gallbladder inflammation against *Murphy's triad*; or a sign against the disease it points to)"),
("A practice against a product used in it (\"recreational use of nitrous oxide\" against \"a cartridge of nitrous oxide\") is `DIFFERENT_SENSE`, never overlapping. A definition that also reports a historical or legal status the other omits (\"now banned in many countries\")",
 "A sign against the disease it indicates (\"Trousseau sign of malignancy, a recurring clot pattern\" against \"a cancer that causes clots\") is `DIFFERENT_SENSE`, never overlapping. A definition that also reports a historical or naming status the other omits (\"now an obsolete diagnosis\")"),
]
S['judging/HUMAN-JUDGE-INSTRUCTIONS.md']=[
(re.compile(r"The Drugs and Recreational Drug Use Lexicon is .*?it never guesses who uses one\."),
 "The Disease, Syndromes and Symptoms Lexicon is a descriptive dictionary of diseases, syndromes, symptoms and medical signs, built from 1,079 Wikipedia pages in the categories Diseases and disorders, Infectious diseases, Infectious diseases by mode of transmission, Symptoms, Syndromes and Medical signs. It says what each term **is**, at a high level. It never gives medical advice, and it never explains how a pathogen could be made, spread or enhanced."),
(re.compile(r"- \*\*Describe, don't advise\.\*\*.*"),
 "- **Describe, don't advise.** You are judging whether two dictionary definitions mean the same thing. Please don't judge whether a treatment or policy is good or bad, and don't add how a disease could be spread or a pathogen made or enhanced. If the assistant is asked for medical advice, it won't give it during the session."),
(re.compile(r"- \*\*No personal details or guesses about groups\.\*\*.*"),
 "- **No personal health details.** Never mention anyone's own health, symptoms or diagnoses, including yours or anyone you know, in your answers or comments. If an item seems to contain such details, say \"Not sure\", tell the assistant \"possible identifiable health information\", and don't repeat it."),
]
S['judging/INTERVIEWER-PROTOCOL.md']=[
("for the drugs lexicon agreement study","for the disease, syndromes and symptoms lexicon agreement study"),
("   personal drug-use details and demographic guesses, which are never stored; see rule 9).","   personal health details, which are never stored; see rule 9)."),
("""8. The lexicon is descriptive only. Do not give drug or medical advice, or any synthesis, procurement, dosing
   or concealment information, and do not give opinions on whether a drug, practice or policy is good, even if
   asked;""","""8. The lexicon is descriptive only. Do not give medical, diagnostic or treatment advice, or any pathogen
   engineering, propagation, enhancement, dissemination or detection-evasion information, and do not give
   opinions on whether a treatment or policy is good, even if asked;"""),
("""9. Never ask for, record or repeat details of an identifiable person's drug use (including the judge's), and
   never infer demographics from individual mentions. If the judge or an item mentions such details, do not
   store them: record UNSURE with notes "possible demographic inference or personal information (not stored)\"""",
 """9. Never ask for, record or repeat details of an identifiable person's health, symptoms or medical records
   (including the judge's). If the judge or an item mentions such details, do not
   store them: record UNSURE with notes "possible identifiable health information (not stored)\""""),
]
S['judging/README.md']=[
("of the Drugs and Recreational Drug Use Lexicon (352 seeds","of the Disease, Syndromes and Symptoms Lexicon (1,079 seeds"),
(ORIGIN_OLD,ORIGIN_NEW),
("(descriptive only; no synthesis, procurement, dosing or concealment guidance; no demographic inference)","(descriptive only; no pathogen engineering, propagation, enhancement, dissemination or detection-evasion detail; no personal health information)"),
(re.compile(r"- \*\*Descriptive only\.\*\* Entries describe.*"),
 "- **Descriptive only.** Entries describe diseases, syndromes, symptoms and signs at a high level. Judges compare meanings; they never add pathogen engineering, propagation, enhancement, dissemination or detection-evasion details, and give no medical advice."),
(re.compile(r"- \*\*No demographic inference, no personal details\.\*\*.*"),
 "- **No personal health information.** No judge, model or person writes, requests or uses details of an identifiable person's health or medical records. An item that appears to contain such details is labelled `UNSURE` with the note \"possible identifiable health information\" and reported to the operator, without repeating it."),
]
S['judging/START-HERE-AI-JUDGE.md']=[
("`nikbearbrown/drugs-and-recreational-drug-use-lexicon`","`nikbearbrown/disease-syndromes-and-symptoms-lexicon`"),
("""entries for drugs and
recreational drug use agree in meaning. Do not use the web. The dictionary is descriptive only: judge
meaning, never give synthesis, procurement, dosing or concealment guidance or drug advice, never infer
demographics from individual mentions, and never write or ask for details of a person's drug use.""",
"""entries for diseases,
syndromes, symptoms and medical signs agree in meaning. Do not use the web. The dictionary is descriptive
only: judge meaning, never give pathogen engineering, propagation, enhancement, dissemination or
detection-evasion detail or medical advice, and never write or ask for details of a person's health."""),
]
S['scripts/agreement.py']=[
("(Drugs and Recreational Drug Use Lexicon)","(Disease, Syndromes and Symptoms Lexicon)"),
("Adapted from nikbearbrown/clinical-treatments-and-procedures-lexicon (branch grok-agreement-method, 51774fbd; itself\nported from",
 "Adapted from nikbearbrown/drugs-and-recreational-drug-use-lexicon (branch grok-agreement-method, ab14590; itself\nadapted from nikbearbrown/clinical-treatments-and-procedures-lexicon, 51774fbd, and ported from"),
('r"\\((drugs?|smoking|behaviou?r|drug culture|medicine|medical|organi[sz]ation|slang|substance)\\)"',
 'r"\\((diseases?|disorder|syndrome|symptom|medicine|medical|medical sign|sign|pathology|infection|condition|organi[sz]ation)\\)"'),
(re.compile(r'CAT_CLASS = \{.*?missing at retrieval\.', re.S),
 '''CAT_CLASS = {"Category:Diseases and disorders": "diseases-and-disorders", "Category:Infectious diseases": "infectious-diseases",
             "Category:Infectious diseases by mode of transmission": "infectious-diseases-by-mode-of-transmission",
             "Category:Symptoms": "symptoms", "Category:Syndromes": "syndromes", "Category:Medical signs": "medical-signs"}
# Category:Disease and Category:Diseases were empty and Category:Infectious disease was missing at retrieval;
# Category:Infectious diseases by type of pathogen has no direct article members. None contributes seeds.'''),
(re.compile(r'# trap concepts .*?\nKIND_LABEL = \{.*?\}\n', re.S), None),
]
TRAP='''# trap concepts (AGREEMENT-METHOD.md 4.3). DRAFT FOR BEAR'S REVIEW: proposed by Grok Bot, which also drafted the
# grok edition, so the maintainer should confirm or replace the list before the first run. Chosen from seed titles:
# look-alike signs and syndromes (Abadie's sign of exophthalmic goiter / of tabes dorsalis; Broadbent sign / Broadbent
# inverted sign; Boas' point / Boas' sign; Murphy's sign / Murphy's triad; Hutchinson's sign / teeth / triad;
# Parinaud's syndrome / Parinaud's oculoglandular syndrome; Miller Fisher / Miller-Dieker syndrome; Craniosynostosis-
# anal anomalies-porokeratosis / CDAGS syndrome; Post-traumatic epilepsy / Post-traumatic seizure; Rochon-Duvigneaud's
# / Superior orbital fissure syndrome; Postdrome / Prodrome; Griscelli syndrome type 2 / 3), names that a symptom,
# sign or finding shares with a disease or syndrome (Hyperprolactinaemia, Torticollis / Sandifer syndrome, Infantile
# epileptic spasms syndrome, Trousseau sign of malignancy, Wilkinson's syndrome, Neoplasm) and umbrella terms (Disease,
# Syndrome, Signs and symptoms, Infection, Lesion, Overlap syndrome, Tropical disease, Zoonosis, Vital signs,
# Respiratory tract infection).
TRAP_IDS = {%s}
KIND_LABEL = {"diseases-and-disorders": "Diseases and disorders", "infectious-diseases": "Infectious diseases",
              "infectious-diseases-by-mode-of-transmission": "Infectious diseases by mode of transmission",
              "symptoms": "Symptoms", "syndromes": "Syndromes", "medical-signs": "Medical signs",
              "multiple": "more than one of Diseases and disorders, Infectious diseases, Infectious diseases by mode of "
                          "transmission, Symptoms, Syndromes, Medical signs"}
'''
import csv
seeds={r['preferred_name']:r['concept_id'] for r in csv.DictReader(open('../data/seeds.tsv'),delimiter='\t')}
names=["Abadie's sign of exophthalmic goiter","Abadie's sign of tabes dorsalis","Broadbent sign","Broadbent inverted sign","Boas' point","Boas' sign",
"Murphy's sign","Murphy's triad","Hutchinson's sign","Hutchinson's teeth","Hutchinson's triad","Parinaud's syndrome","Parinaud's oculoglandular syndrome",
"Miller Fisher syndrome","Miller–Dieker syndrome","Craniosynostosis–anal anomalies–porokeratosis syndrome","CDAGS syndrome","Post-traumatic epilepsy",
"Post-traumatic seizure","Rochon-Duvigneaud's syndrome","Superior orbital fissure syndrome","Postdrome","Prodrome","Griscelli syndrome type 2","Griscelli syndrome type 3",
"Hyperprolactinaemia","Torticollis","Sandifer syndrome","Infantile epileptic spasms syndrome","Trousseau sign of malignancy","Wilkinson's syndrome","Neoplasm",
"Disease","Syndrome","Signs and symptoms","Infection","Lesion","Overlap syndrome","Tropical disease","Zoonosis","Vital signs","Respiratory tract infection"]
ids=[seeds[n] for n in names]
idtxt=', '.join('"%s"'%i for i in ids)
# wrap
parts=[];line='';
for tok in ['"%s"'%i for i in ids]:
    if len(line)+len(tok)+2>100: parts.append(line); line=''
    line+=tok+', '
parts.append(line.rstrip(', '))
idtxt='\n            '.join(p.rstrip() for p in parts)
TRAPTXT=TRAP%idtxt
for f in ['AGREEMENT-METHOD.md','judging/AI-JUDGE-INSTRUCTIONS.md','judging/prompts/system.txt','judging/prompts/P1.txt','judging/prompts/P2.txt','judging/prompts/P3.txt']:
    S.setdefault(f,[]); S[f]=COMMON+S[f] if f in('AGREEMENT-METHOD.md','judging/AI-JUDGE-INSTRUCTIONS.md') else COMMON
bad=0
for f,subs in S.items():
    t=(R/f).read_text()
    for old,new in subs:
        if new is None: new=TRAPTXT
        if isinstance(old,str):
            if old not in t:
                if (old,new) in COMMON: continue
                print('MISSING',f,old[:60]); bad=1; continue
            t=t.replace(old,new)
        else:
            t2,n=old.subn(lambda m:new,t)
            if n==0: print('MISSING',f,old.pattern[:60]); bad=1
            t=t2
    (R/f).write_text(t)
print('trap ids',len(ids)); sys.exit(bad)
