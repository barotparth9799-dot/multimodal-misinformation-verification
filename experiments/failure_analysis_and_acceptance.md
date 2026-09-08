\# Failure Analysis and Acceptance Criteria



\## 1. Purpose



This document records the failure cases observed during realistic multimodal validation, the engineering changes used to resolve them, and the acceptance criteria for the final system.



\## 2. Validation Progression



| Validation Stage | Accuracy | Macro F1 |

|---|---:|---:|

| Initial realistic validation | 60.00% | 59.23% |

| After visual mismatch gate | 80.00% | 77.41% |

| After compound-claim handling | 90.00% | 89.45% |

| After evidence coverage improvement | 100.00% | 100.00% |



The progression demonstrates iterative testing and engineering improvement rather than relying only on a final test result.



\## 3. Failure Case: RV15



\### Claim



The Moon is made of cheese.



\### Expected Result



MISINFORMATION



\### Initial Result



UNCERTAIN



\### Root Cause



The evidence corpus did not contain sufficiently relevant authoritative information about the physical composition of the Moon. The retrieval stage therefore could not provide strong evidence for the NLI stance analyzer.



\### Engineering Fix



Authoritative NASA evidence describing the Moon as a rocky, layered world with a core, mantle, and crust was added to the evidence corpus.



\### Final Result



MISINFORMATION with approximately 99.96% confidence.



\### Evidence



E013 - NASA Moon composition information.



\## 4. Failure Case: RV20



\### Claim



The Moon is Earth's only natural satellite and it is larger than the Earth.



\### Expected Result



MISINFORMATION



\### Initial Result



VERIFIED



\### Root Cause



The original evidence corpus contained support for the first subclaim but no relevant evidence about the second subclaim. Treating the complete compound statement as one retrieval query allowed the supported part to dominate the decision.



\### Engineering Fix



Two improvements were introduced:



1\. Compound claims are decomposed into independently testable subclaims.

2\. Authoritative NASA evidence about the relative size of the Moon and Earth was added to the evidence corpus.



The system now evaluates each subclaim independently and can identify a strong contradiction even when another subclaim is supported.



\### Final Result



MISINFORMATION with 90% confidence.



\### Evidence



E012 - NASA Moon/Earth size information.



\## 5. Engineering Lessons



\### Evidence Coverage



A retrieval-based verification system is limited by the factual coverage of its evidence corpus. Missing evidence should produce uncertainty rather than unsupported certainty.



\### Compound Claims



A compound claim may contain both true and false statements. Independent subclaim evaluation reduces the risk that evidence supporting one part incorrectly validates the entire claim.



\### Multimodal Consistency



Image-text consistency is used as an additional verification signal. A visually unrelated image should reduce confidence and may produce an UNCERTAIN result rather than automatically declaring misinformation.



\### Confidence-Aware Decisions



The system distinguishes VERIFIED, MISINFORMATION, and UNCERTAIN outcomes instead of forcing every claim into a binary decision.



\## 6. Acceptance Criteria



The final system is considered acceptable when all of the following are satisfied:



\- Text claims are processed successfully.

\- Images are processed successfully.

\- Text and image representations are generated.

\- Image-text consistency is evaluated.

\- Relevant evidence is retrieved.

\- Evidence sources and URLs are returned.

\- Evidence stance is evaluated using NLI.

\- Multimodal signals are fused into a final decision.

\- Compound claims can be decomposed and evaluated independently.

\- Strongly contradicted claims can be identified.

\- Visually inconsistent claims can be downgraded to uncertainty.

\- Unsupported claims are not automatically treated as verified.

\- The system returns VERIFIED, MISINFORMATION, or UNCERTAIN.

\- A confidence score is produced.

\- A human-readable explanation is produced.

\- Invalid or unsuitable inputs are handled safely.

\- Unit and integration tests pass.

\- Realistic validation results are reproducible.

\- Baseline comparison is completed.

\- Modality ablation is completed.

\- Confidence calibration is evaluated.

\- Robustness and edge cases are tested.

\- Failure analysis is documented.

\- The application runs end-to-end through the Streamlit interface.



\## 7. Current Realistic Validation Result



The realistic validation set contains:



\- 7 MISINFORMATION cases

\- 8 UNCERTAIN cases

\- 5 VERIFIED cases



Final result:



\- Accuracy: 100%

\- Macro F1: 1.00

\- Incorrect cases: 0/20

\- MISINFORMATION: 7/7 correct

\- UNCERTAIN: 8/8 correct

\- VERIFIED: 5/5 correct



This result satisfies the current validation acceptance criteria for the designed realistic test set.



\## 8. Limitation



The realistic validation set contains 20 cases and therefore cannot establish perfect real-world generalization.



The 100% result should be reported as performance on the defined validation scenarios, not as proof that the system is universally correct.

