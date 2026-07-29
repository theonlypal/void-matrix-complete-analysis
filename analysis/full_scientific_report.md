# Full scientific report

**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**


## Table of contents

1. Abstract
2. Operational definition
3. Methods and provenance
4. Integrity and outcome flow
5. All-Void Results
6. Void Subtype Results
7. Normal-Stop Void Counts
8. Output-Budget-Stop Void Counts
9. Model and provider morphology
10. Dependence sensitivity
11. Scope, limitations, and reproducibility

## 1. Abstract

The prospectively frozen confirmatory design scheduled and completed
**31,430/31,430** final trials across 11 models and four providers. The frozen
terminal verifier exhaustively verified **31,484** raw records. Independent
analysis replayed **62,968** event hashes, reclassified all final trials, and
audited **1,257** claim-directed raw records with zero anomalies.

All Void subtypes occurred in **11,658/31,430
(37.09%)** final trials:
V0=7,328,
V1=2,565,
V2=1,765, and
VU=0.
Strict matched semantic null/control pairs and the
4,000-token logical contrast quantify selectivity while preserving pair-level
dependence.

## 2. Operational definition

A Void is a model execution returning a successful provider response with exactly zero visible UTF-8 output bytes. Provider termination metadata determines its subtype. Explicit refusals, safety blocks, tool-mediated executions, and transport, protocol, billing, quota, rate-limit, and infrastructure failures are distinct non-Void outcomes.

## Void taxonomy

| Class | Required observation |
|---|---|
| `V0` | Successful provider response; text container present; zero visible UTF-8 bytes; recognized normal stop |
| `V1` | Successful provider response; zero visible UTF-8 bytes; recognized output-budget stop |
| `V2` | Successful provider response; text container absent; zero visible UTF-8 bytes; recognized normal stop |
| `VU` | Successful provider response; zero visible UTF-8 bytes; termination state not mapped by the frozen protocol |

All four classes retain Void status. Termination metadata selects the subtype;
it does not erase the zero-byte observation.

**Near-Voids are non-Voids:** whitespace, invisible Unicode, punctuation-only output, ellipses, and every other nonempty output remain outside the Void class.

## 3. Methods and provenance

- Evidence Git commit: `2dfe895bdafd35d23d6dab5f307ed560214a3843` (2026-07-25T20:11:56-07:00)
- Frozen runner SHA-256: `a0db4b10785783102dd9d2ea51814e02c8447a004f2843541545e54a5365530a`
- Public schedule seed: `void-matrix-confirmatory-2026-07-27-sharthok-rayan-pal`
- Seed SHA-256: `3a81b5651d471465e9f24c1fac3368125d964d1964c2cea1621bc32952fca2a2`
- Schedule SHA-256: `2c23670ecf2d845ac2af2c5890f12f60b8b008b4ac2d32e90214608c12c09e20`
- Frozen manifest reference: `90d02559470c33d05e6d0baceaddd58ce4e26b48f67adc9ecb56509823aaa462`
- Final event-chain SHA-256: `acf4b13af758784f657075ee7a9dda3192ccba45d025d033bc443e4bbe4d18d9`

The public seed is not metadata-only: the frozen runner hashes the UTF-8 seed,
converts the digest to an integer, seeds `random.Random`, and shuffles the
complete regenerated slot universe. Verification reconstructs and compares the
ordered schedule. No external preregistration record was identified; the
correct description is **prospectively frozen confirmatory design**.

The complete status classification of every analysis is recorded in
`analysis_scope.md`. Confirmatory contrasts are separated from prespecified
secondary analyses, exploratory post-run groupings, descriptive census results,
robustness sensitivities, and integrity checks.

## 4. Integrity and outcome flow

| flow_node | count | parent | definition |
|---|---|---|---|
| scheduled_slots | 31430 |  | sealed schedule |
| attempts_initiated | 31484 | scheduled_slots | includes retry attempts |
| additional_retry_attempts | 54 | attempts_initiated | raw attempts beyond one per final slot |
| recovered_final_slots | 53 | final_completed_slots | 52 completed on attempt 2; 1 on attempt 3 |
| final_completed_slots | 31430 | scheduled_slots | exactly one final completion per slot |
| successful_http_final_slots | 31404 | final_completed_slots | HTTP 2xx final observations |
| operational_nonvoid_final_slots | 26 | final_completed_slots | BE/QE/E/PI |
| successful_classified_outcomes | 31404 | final_completed_slots | all non-operational final classes |
| class_V0 | 7328 | final_completed_slots | frozen terminal classification |
| class_V1 | 2565 | final_completed_slots | frozen terminal classification |
| class_V2 | 1765 | final_completed_slots | frozen terminal classification |
| class_VU | 0 | final_completed_slots | frozen terminal classification |
| class_NV | 2348 | final_completed_slots | frozen terminal classification |
| class_R | 16562 | final_completed_slots | frozen terminal classification |
| class_RF | 835 | final_completed_slots | frozen terminal classification |
| class_SB | 1 | final_completed_slots | frozen terminal classification |
| class_TC | 0 | final_completed_slots | frozen terminal classification |
| class_BE | 25 | final_completed_slots | frozen terminal classification |
| class_QE | 0 | final_completed_slots | frozen terminal classification |
| class_E | 1 | final_completed_slots | frozen terminal classification |
| class_PI | 0 | final_completed_slots | frozen terminal classification |

The final classes sum to 31,430. The event ledger contains 31,484 starts, 31,430
final completions, and 54 completed retry-attempt records. Fifty-three final
slots were recovered after an earlier attempt (52 on attempt 2 and one on
attempt 3). Incomplete attempts and orphan raw records are both zero.

## 5. All-Void Results

### 5.1 Strict matched semantic pairs

| pair_count | both_outcome | exposed_only | control_only | neither | discordant_pairs | exact_mcnemar_p | exact_mcnemar_log10_p | exact_mcnemar_p_display | discordant_direction_rate | discordant_direction_ci95_low | discordant_direction_ci95_high | discordant_direction_ci_method | paired_risk_difference | paired_risk_difference_ci95_low | paired_risk_difference_ci95_high | paired_risk_difference_ci_method | group_type | group_value | outcome | exposed_numerator | exposed_denominator | control_numerator | control_denominator | unpaired_risk_exposed | unpaired_risk_control | unpaired_risk_difference | unpaired_risk_difference_ci95_low | unpaired_risk_difference_ci95_high | unpaired_risk_ratio | unpaired_risk_ratio_ci95_low | unpaired_risk_ratio_ci95_high | unpaired_odds_ratio | unpaired_odds_ratio_ci95_low | unpaired_odds_ratio_ci95_high | unpaired_zero_cell_correction |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4290 | 0 | 2505 | 0 | 1785 | 2505 | 0 | -753.779 | p < 10^-753; log10(p)=-753.779109 | 1 | 0.998528 | 1 | Clopper-Pearson exact | 0.583916 | 0.569166 | 0.598666 | paired binary Wald interval | pooled | all | any_void | 2505 | 4290 | 0 | 4290 | 0.583916 | 0 | 0.583916 | 0.569166 | 0.598666 | 5011 | 313.447 | 80109.7 | 12041.3 | 752.546 | 192669 | Haldane-Anscombe 0.5 |

The strict matched denominator is **4,290 pairs**. It is distinct from the
**12,340** total output-licensed control trials used only in the broader
analysis-defined role contrast.

## 6. Void Subtype Results

| classification | count | rate |
|---|---|---|
| V0 | 7328 | 0.233153 |
| V1 | 2565 | 0.0816099 |
| V2 | 1765 | 0.0561565 |
| VU | 0 | 0 |
| NV | 2348 | 0.0747057 |
| R | 16562 | 0.526949 |
| RF | 835 | 0.026567 |
| SB | 1 | 3.18167e-05 |
| TC | 0 | 0 |
| BE | 25 | 0.000795418 |
| QE | 0 | 0 |
| E | 1 | 3.18167e-05 |
| PI | 0 | 0 |

All four classes retain Void status. Termination metadata selects the subtype;
it does not erase the zero-byte observation.

## 7. Normal-Stop Void Counts

Normal-stop Voids (V0+V2) occurred in **9,093/31,430
(28.93%)** final trials.

V0+V2 are the normal-stop Void subtypes. Their presence shows that recognized output-budget termination does not explain all Voids.

### 7.1 Strict matched semantic pairs

| pair_count | both_outcome | exposed_only | control_only | neither | discordant_pairs | exact_mcnemar_p | exact_mcnemar_log10_p | exact_mcnemar_p_display | discordant_direction_rate | discordant_direction_ci95_low | discordant_direction_ci95_high | discordant_direction_ci_method | paired_risk_difference | paired_risk_difference_ci95_low | paired_risk_difference_ci95_high | paired_risk_difference_ci_method | group_type | group_value | outcome | exposed_numerator | exposed_denominator | control_numerator | control_denominator | unpaired_risk_exposed | unpaired_risk_control | unpaired_risk_difference | unpaired_risk_difference_ci95_low | unpaired_risk_difference_ci95_high | unpaired_risk_ratio | unpaired_risk_ratio_ci95_low | unpaired_risk_ratio_ci95_high | unpaired_odds_ratio | unpaired_odds_ratio_ci95_low | unpaired_odds_ratio_ci95_high | unpaired_zero_cell_correction |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4290 | 0 | 2504 | 0 | 1786 | 2504 | 0 | -753.478 | p < 10^-753; log10(p)=-753.478079 | 1 | 0.998528 | 1 | Clopper-Pearson exact | 0.583683 | 0.568932 | 0.598434 | paired binary Wald interval | pooled | all | normal_stop_V0_V2 | 2504 | 4290 | 0 | 4290 | 0.583683 | 0 | 0.583683 | 0.568932 | 0.598434 | 5009 | 313.322 | 80077.7 | 12029.7 | 751.824 | 192484 | Haldane-Anscombe 0.5 |

### 7.2 Logical null/yes contrast

The 4,000-token normal-stop logical contrast was:

| pair_count | both_outcome | exposed_only | control_only | neither | discordant_pairs | exact_mcnemar_p | exact_mcnemar_log10_p | exact_mcnemar_p_display | discordant_direction_rate | discordant_direction_ci95_low | discordant_direction_ci95_high | discordant_direction_ci_method | paired_risk_difference | paired_risk_difference_ci95_low | paired_risk_difference_ci95_high | paired_risk_difference_ci_method | group_type | group_value | outcome | exposed_numerator | exposed_denominator | control_numerator | control_denominator | unpaired_risk_exposed | unpaired_risk_control | unpaired_risk_difference | unpaired_risk_difference_ci95_low | unpaired_risk_difference_ci95_high | unpaired_risk_ratio | unpaired_risk_ratio_ci95_low | unpaired_risk_ratio_ci95_high | unpaired_odds_ratio | unpaired_odds_ratio_ci95_low | unpaired_odds_ratio_ci95_high | unpaired_zero_cell_correction | interpretive_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1100 | 0 | 523 | 0 | 577 | 523 | 7.28354e-158 | -157.138 | 7.28353587031e-158; log10(p)=-157.137658 | 1 | 0.992972 | 1 | Clopper-Pearson exact | 0.475455 | 0.445943 | 0.504966 | paired binary Wald interval | budget | 4000 | normal_stop_V0_V2 | 523 | 1100 | 0 | 1100 | 0.475455 | 0 | 0.475455 | 0.445943 | 0.504966 | 1047 | 65.4844 | 16740 | 1995.19 | 124.404 | 31998.8 | Haldane-Anscombe 0.5 | budget-controlled logical contrast |

The 100-token normal-stop logical contrast was:

| pair_count | both_outcome | exposed_only | control_only | neither | discordant_pairs | exact_mcnemar_p | exact_mcnemar_log10_p | exact_mcnemar_p_display | discordant_direction_rate | discordant_direction_ci95_low | discordant_direction_ci95_high | discordant_direction_ci_method | paired_risk_difference | paired_risk_difference_ci95_low | paired_risk_difference_ci95_high | paired_risk_difference_ci_method | group_type | group_value | outcome | exposed_numerator | exposed_denominator | control_numerator | control_denominator | unpaired_risk_exposed | unpaired_risk_control | unpaired_risk_difference | unpaired_risk_difference_ci95_low | unpaired_risk_difference_ci95_high | unpaired_risk_ratio | unpaired_risk_ratio_ci95_low | unpaired_risk_ratio_ci95_high | unpaired_odds_ratio | unpaired_odds_ratio_ci95_low | unpaired_odds_ratio_ci95_high | unpaired_zero_cell_correction | interpretive_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1100 | 0 | 158 | 0 | 942 | 158 | 5.47382e-48 | -47.2617 | 5.47382212627e-48; log10(p)=-47.261709 | 1 | 0.976923 | 1 | Clopper-Pearson exact | 0.143636 | 0.12291 | 0.164362 | paired binary Wald interval | budget | 100 | normal_stop_V0_V2 | 158 | 1100 | 0 | 1100 | 0.143636 | 0 | 0.143636 | 0.12291 | 0.164362 | 317 | 19.7664 | 5083.83 | 370.142 | 23.0196 | 5951.65 | Haldane-Anscombe 0.5 | budget-sensitive stress condition |

Model-, provider-, budget-, study-, and pair-stratified results are in
`tables/matched_analysis.csv` and `tables/logical_analysis.csv`.

## 8. Output-Budget-Stop Void Counts

Output-budget-stop Voids (V1) occurred in
**2,565/31,430
(8.16%)** final trials.
V1 has the same Void status as V0, V2, and VU.

## 9. Model and provider morphology

### By model

| provider | model_id | trials | voids | void_rate | normal_stop_voids | normal_stop_void_rate | V0 | V1 | V2 | VU | responses | near_voids | refusals | safety_blocks | tool_calls | operational_nonvoid | recovered_retries | returned_model_match_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openai | gpt-4-0613 | 3130 | 1276 | 0.407668 | 1276 | 0.407668 | 1276 | 0 | 0 | 0 | 1739 | 115 | 0 | 0 | 0 | 0 | 2 | 1 |
| openai | gpt-5.2-2025-12-11 | 3180 | 1489 | 0.468239 | 1489 | 0.468239 | 1489 | 0 | 0 | 0 | 1427 | 264 | 0 | 0 | 0 | 0 | 3 | 1 |
| openai | gpt-5.5-2026-04-23 | 2680 | 1281 | 0.477985 | 1098 | 0.409701 | 1098 | 183 | 0 | 0 | 1378 | 9 | 0 | 0 | 0 | 12 | 1 | 0.995522 |
| openai | gpt-5.6-luna | 2680 | 929 | 0.346642 | 818 | 0.305224 | 818 | 111 | 0 | 0 | 1634 | 116 | 0 | 0 | 0 | 1 | 1 | 0.999627 |
| openai | gpt-5.6-sol | 2680 | 689 | 0.25709 | 602 | 0.224627 | 602 | 87 | 0 | 0 | 1528 | 453 | 0 | 0 | 0 | 10 | 1 | 0.996269 |
| openai | gpt-5.6-terra | 2680 | 1100 | 0.410448 | 1006 | 0.375373 | 1006 | 94 | 0 | 0 | 1547 | 31 | 0 | 0 | 0 | 2 | 3 | 0.999254 |
| anthropic | claude-opus-4-6 | 3180 | 1266 | 0.398113 | 1266 | 0.398113 | 0 | 0 | 1266 | 0 | 1826 | 88 | 0 | 0 | 0 | 0 | 7 | 1 |
| anthropic | claude-fable-5 | 2680 | 725 | 0.270522 | 352 | 0.131343 | 352 | 373 | 0 | 0 | 1080 | 200 | 675 | 0 | 0 | 0 | 21 | 1 |
| anthropic | claude-opus-5 | 2680 | 1009 | 0.376493 | 327 | 0.122015 | 327 | 682 | 0 | 0 | 1317 | 194 | 160 | 0 | 0 | 0 | 3 | 1 |
| google | gemini-3.5-flash | 3180 | 747 | 0.234906 | 499 | 0.156918 | 0 | 248 | 499 | 0 | 1818 | 614 | 0 | 1 | 0 | 0 | 6 | 1 |
| moonshot | kimi-k3 | 2680 | 1147 | 0.427985 | 360 | 0.134328 | 360 | 787 | 0 | 0 | 1268 | 264 | 0 | 0 | 0 | 1 | 5 | 0.999627 |

### By provider

| provider | total | V0 | V1 | V2 | VU | NV | R | RF | SB | TC | BE | QE | E | PI | void_total | normal_stop_void_total | budget_stop_void_total | void_rate | normal_stop_void_rate | successful_http |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| moonshot | 2680 | 360 | 787 | 0 | 0 | 264 | 1268 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1147 | 360 | 787 | 0.427985 | 0.134328 | 2679 |
| openai | 17030 | 6289 | 475 | 0 | 0 | 988 | 9253 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 6764 | 6289 | 475 | 0.397181 | 0.369289 | 17005 |
| anthropic | 8540 | 679 | 1055 | 1266 | 0 | 482 | 4223 | 835 | 0 | 0 | 0 | 0 | 0 | 0 | 3000 | 1945 | 1055 | 0.351288 | 0.227752 | 8540 |
| google | 3180 | 0 | 248 | 499 | 0 | 614 | 1818 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 747 | 499 | 248 | 0.234906 | 0.156918 | 3180 |

Requested/returned identifier denominators and all missing identifiers are
accounted for in `tables/returned_model_accounting.csv`; substantive returned
identifier mismatches equal **0**.

## 10. Dependence sensitivity

The paired exact analyses preserve pair-level dependence. Cluster bootstraps
resample whole models or providers. GEE sensitivity models use an independence working correlation
with sandwich covariance and separately cluster by model and prompt while
adjusting for budget, system, provider, parameter track, and study.

| outcome | cluster | cluster_count | n | formula | working_correlation | covariance | status | iterations | coefficient_log_odds | robust_se | odds_ratio | odds_ratio_ci95_low | odds_ratio_ci95_high | p_value | error |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| void_observed | model_id | 11 | 26590 | void_observed ~ null_condition + C(budget) + C(system_id) + C(provider) + C(parameter_track) + C(study_id) | independence | GEE sandwich/robust | nonfinite | 200 | nan | nan | nan | nan | nan | nan | GEE returned nonfinite null-condition estimates; paired exact and cluster-bootstrap analyses remain authoritative. |
| void_observed | prompt_id | 16 | 26590 | void_observed ~ null_condition + C(budget) + C(system_id) + C(provider) + C(parameter_track) + C(study_id) | independence | GEE sandwich/robust | nonconverged | 200 | 3.62857 | 0.415149 | 37.6589 | 16.6914 | 84.9657 | 2.32277e-18 | GEE reached the iteration limit without convergence; finite estimates are retained only as diagnostics, and paired exact and cluster-bootstrap analyses remain authoritative. |
| normal_stop_void | model_id | 11 | 26590 | normal_stop_void ~ null_condition + C(budget) + C(system_id) + C(provider) + C(parameter_track) + C(study_id) | independence | GEE sandwich/robust | nonfinite | 200 | nan | nan | nan | nan | nan | nan | GEE returned nonfinite null-condition estimates; paired exact and cluster-bootstrap analyses remain authoritative. |
| normal_stop_void | prompt_id | 16 | 26590 | normal_stop_void ~ null_condition + C(budget) + C(system_id) + C(provider) + C(parameter_track) + C(study_id) | independence | GEE sandwich/robust | nonfinite | 200 | nan | nan | nan | nan | nan | nan | GEE returned nonfinite null-condition estimates; paired exact and cluster-bootstrap analyses remain authoritative. |

Failures, if any, are retained verbatim rather than silently omitted. Complete
effect estimates and arbitrary-range exact-probability displays are in
`statistical_tables.csv`.

## 11. Scope, limitations, and reproducibility

The evidence establishes black-box API behavior within the frozen model,
provider, prompt, language, and serving-stack scope. It does not identify an
internal mechanism, prove shared latent representations, or establish agency.
Proprietary serving stacks
can drift, prompt categories require independent replication, and repeated
trials are not independent model samples.

The original and hardened environments are recorded separately in
`environment_comparison.md`. Cross-environment reproduction uses normalized
semantic equivalence for original headline numerators, denominators, class
totals, matched pairs, and logical pairs. Byte identity is claimed only for
fresh reruns within the same hardened environment after it is actually tested.
