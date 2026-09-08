\# Multimodal Misinformation Verification

\# Final Evaluation Dossier



\## 1. Purpose



This document consolidates the experimental evaluation of the Multimodal Misinformation Verification system.



The evaluation examines:



\- Classification performance

\- Macro F1

\- Confusion matrix

\- Confidence calibration

\- Baseline comparison

\- Modality ablation

\- Robustness

\- Realistic multimodal validation

\- Failure analysis

\- Acceptance criteria

\- Reproducibility

\- System limitations



The objective is to evaluate the complete multimodal verification pipeline rather than only an individual model.



\---



\## 2. Evaluation Categories



The project uses multiple evaluation levels:



1\. Unit testing

2\. Controlled validation

3\. Baseline comparison

4\. Modality ablation

5\. Robustness and edge-case testing

6\. Realistic multimodal validation

7\. Failure analysis



Using multiple evaluation methods reduces the risk of judging the system using a single metric.



\---



\## 3. Automated Software Testing



The project includes automated unit tests covering major components.



Tested components include:



\- Text processing

\- Text encoding

\- Image encoding

\- Visual topic analysis

\- Visual consistency

\- Evidence encoding

\- FAISS retrieval

\- NLI stance analysis

\- Multimodal fusion

\- Verification

\- Explanation

\- Claim decomposition

\- End-to-end pipeline

\- Robustness and edge cases



The project also uses continuous integration to run compilation and automated tests.



\---



\## 4. Controlled Validation Dataset



The controlled validation set contains:



`15 cases`



The three possible labels are:



\- VERIFIED

\- MISINFORMATION

\- UNCERTAIN



The controlled dataset was designed to test different combinations of textual evidence and visual information.



\---



\## 5. Controlled Validation Results



Final controlled validation performance:



| Metric | Result |

|---|---:|

| Accuracy | 86.67% |

| Macro F1 | 87.50% |

| Correct cases | 13/15 |

| Incorrect cases | 2/15 |



These results demonstrate that the system can combine evidence retrieval and visual consistency signals to make useful verification decisions.



\---



\## 6. Confusion Matrix



The confusion matrix uses the label order:



1\. MISINFORMATION

2\. UNCERTAIN

3\. VERIFIED



Final matrix:



| Actual / Predicted | MISINFORMATION | UNCERTAIN | VERIFIED |

|---|---:|---:|---:|

| MISINFORMATION | 3 | 0 | 0 |

| UNCERTAIN | 0 | 7 | 1 |

| VERIFIED | 0 | 1 | 3 |



The main errors occurred between `UNCERTAIN` and `VERIFIED`.



No MISINFORMATION case was incorrectly classified as VERIFIED in this controlled evaluation.



\---



\## 7. Confidence Calibration



Expected Calibration Error (ECE):



`0.30086`



Mean confidence:



`0.56581`



The calibration result shows that confidence estimates are not perfectly calibrated.



Therefore, confidence should be interpreted as a measure of model decision strength rather than as a guaranteed probability.



Further calibration improvement would be appropriate for a production-grade system.



\---



\## 8. Baseline Comparison



Three major configurations were compared.



| Configuration | Accuracy | Macro F1 |

|---|---:|---:|

| Evidence-only | 60.00% | 65.71% |

| Image-only | 53.33% | 23.19% |

| Full multimodal | 86.67% | 87.50% |



The full multimodal configuration performed substantially better than either individual baseline on the controlled dataset.



\---



\## 9. Modality Ablation



The following configurations were evaluated:



| Configuration | Accuracy | Macro F1 |

|---|---:|---:|

| Evidence-only | 60.00% | 65.71% |

| Image-only | 53.33% | 23.19% |

| Evidence + Image Consistency | 86.67% | 87.50% |

| Full Multimodal | 86.67% | 87.50% |



Adding image-text consistency to evidence-based verification improved controlled-set accuracy by:



`26.67 percentage points`



Macro F1 improved by:



`21.79 percentage points`



The full multimodal configuration produced the same score as the evidence plus image-consistency configuration on this dataset.



This does not prove that every component will independently improve results on every future dataset.



\---



\## 10. Realistic Multimodal Validation



A separate realistic validation set contains:



`20 cases`



The test cases include:



\- True factual claims

\- False claims

\- Matching images

\- Mismatched images

\- Ambiguous situations

\- Compound claims

\- Contradictory evidence

\- Missing or weak evidence

\- Visual inconsistency



Final result:



| Metric | Result |

|---|---:|

| Accuracy | 100.00% |

| Macro F1 | 100.00% |

| Correct cases | 20/20 |

| Incorrect cases | 0/20 |



Confusion matrix:



| Actual / Predicted | MISINFORMATION | UNCERTAIN | VERIFIED |

|---|---:|---:|---:|

| MISINFORMATION | 7 | 0 | 0 |

| UNCERTAIN | 0 | 8 | 0 |

| VERIFIED | 0 | 0 | 5 |



\### Important Interpretation



The 100% result applies only to this designed 20-case realistic validation dataset.



It does not prove that the system will achieve 100% accuracy on unrestricted real-world misinformation.



The evidence knowledge base and visual topic coverage remain limited.



\---



\## 11. Examples of Important Validation Cases



\### False factual claim



Example:



`The Moon is a planet.`



Expected result:



`MISINFORMATION`



The system retrieves contradictory evidence and identifies the claim as false.



\---



\### Visual mismatch



A claim about the Moon paired with an unrelated car image should not automatically be considered verified simply because textual evidence exists.



The visual consistency component detects the mismatch and can move the decision toward `UNCERTAIN`.



\---



\### Compound claim



Example:



`The Moon is a planet and Earth's only natural satellite.`



The system decomposes the statement into subclaims.



This prevents one supported statement from hiding another contradicted statement.



\---



\### Strong contradiction



When highly relevant evidence directly contradicts a claim, the verifier can apply contradiction handling and return:



`MISINFORMATION`



with high confidence.



\---



\## 12. Robustness and Edge Cases



The project tests situations including:



\- Empty or invalid input

\- Missing images

\- Unsupported image conditions

\- Unknown visual topics

\- Weak evidence

\- No useful evidence

\- Contradictory evidence

\- Image-text mismatch

\- Compound claims

\- Pronoun-containing compound claims

\- Ambiguous cases



The system is designed to return `UNCERTAIN` when the available information does not support a reliable conclusion.



\---



\## 13. Failure Analysis



Failure analysis identified several important issues during development.



\### Failure 1: Insufficient Moon Evidence



Some Moon-related claims initially lacked sufficiently specific evidence.



Root cause:



The evidence knowledge base did not contain enough Moon composition information.



Improvement:



Additional NASA evidence was added for Moon size and composition.



Result:



The affected validation case became correctly classified.



\---



\### Failure 2: Compound Claim Handling



A compound Moon claim contained multiple factual statements.



The first subclaim was supported while another subclaim lacked sufficient evidence.



Root cause:



The original pipeline did not independently evaluate every subclaim.



Improvement:



A claim decomposition component was added.



Result:



The system can now evaluate compound claims independently and apply a strong contradiction when an important subclaim is false.



\---



\### Failure 3: Image-Claim Mismatch



Textual evidence alone can support a claim while the associated image is unrelated.



Root cause:



A text-only decision would ignore the visual modality.



Improvement:



Visual topic analysis and text-image consistency checking were integrated into the decision process.



\---



\## 14. Acceptance Criteria



The system is considered acceptable for the academic prototype when it demonstrates:



| Requirement | Status |

|---|---|

| Text processing | PASS |

| Text embeddings | PASS |

| Image embeddings | PASS |

| Image-text consistency | PASS |

| Evidence retrieval | PASS |

| Source citations | PASS |

| NLI stance analysis | PASS |

| Multimodal fusion | PASS |

| Compound claim handling | PASS |

| Contradiction handling | PASS |

| Uncertainty handling | PASS |

| Confidence-aware output | PASS |

| Human-readable explanation | PASS |

| Automated tests | PASS |

| Reproducible experiments | PASS |

| Baseline comparison | PASS |

| Modality ablation | PASS |

| Calibration evaluation | PASS |

| Robustness testing | PASS |

| Failure analysis | PASS |

| Streamlit end-to-end workflow | PASS |



\---



\## 15. Reproducibility



The evaluation can be reproduced using:



\- Version-controlled source code

\- `requirements.txt`

\- Experiment scripts

\- Validation datasets

\- Evaluation result files

\- Unit tests

\- CI workflow

\- Documented model configuration



Evaluation artifacts are retained in the repository.



\---



\## 16. Key Findings



The evaluation provides several important findings.



\### Finding 1



The full multimodal system performs better than the evidence-only and image-only baselines on the controlled dataset.



\### Finding 2



Image-text consistency provides an important additional signal when the image does not match the claim.



\### Finding 3



Evidence retrieval and NLI provide the main factual verification signal.



\### Finding 4



Compound claim decomposition improves handling of statements containing multiple facts.



\### Finding 5



The `UNCERTAIN` category is important for handling insufficient evidence and visual mismatch.



\### Finding 6



Confidence estimates require further calibration before being interpreted as reliable probabilities.



\---



\## 17. Limitations



The evaluation has important limitations:



1\. The datasets are relatively small.

2\. The evidence knowledge base covers selected topics.

3\. Visual topic analysis currently supports a limited set of broad topics.

4\. Controlled cases cannot represent all real-world misinformation.

5\. Public evidence sources may change over time.

6\. Model behavior may vary on unseen domains.

7\. Confidence calibration is not perfect.

8\. A 100% score on the realistic validation set does not establish universal generalization.



\---



\## 18. Academic Interpretation



The evaluation demonstrates that the project satisfies the core requirements of a multimodal AI verification prototype.



The system does not depend only on text classification.



Instead, it integrates:



`Text + Image + Evidence Retrieval + NLI + Visual Consistency + Multimodal Fusion + Explanation`



This provides a stronger demonstration of multimodal AI system design.



\---



\## 19. Final Evaluation Statement



The implemented system successfully demonstrates an end-to-end multimodal misinformation verification workflow.



The controlled evaluation achieved:



\- 86.67% accuracy

\- 87.50% Macro F1



The realistic 20-case validation achieved:



\- 100% accuracy

\- 100% Macro F1



The controlled evaluation also demonstrates a substantial improvement over the evidence-only and image-only baselines.



The results support the conclusion that the implemented multimodal pipeline is functional and suitable for academic demonstration.



The results should not be interpreted as proof of universal real-world misinformation detection performance.



\---



\## 20. Evaluation Artifacts



Relevant evaluation artifacts include:



\- Controlled validation data

\- Controlled validation results

\- Realistic validation dataset

\- Realistic validation results

\- Baseline comparison experiment

\- Modality ablation experiment

\- Robustness tests

\- Failure analysis

\- Acceptance criteria

\- Unit test suite

\- CI workflow

\- System/model card

\- Dataset documentation

\- Architecture documentation

