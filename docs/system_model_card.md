\# System and Model Card



\## 1. System Name



Multimodal Misinformation Verification Using Text, Image Consistency and Evidence Retrieval



\---



\## 2. System Overview



This system verifies information by combining multiple signals:



1\. Text analysis

2\. Image analysis

3\. Text-image consistency

4\. Evidence retrieval

5\. Natural Language Inference (NLI)

6\. Multimodal score fusion

7\. Confidence-aware decision making

8\. Human-readable explanations



The purpose is to demonstrate an end-to-end multimodal AI verification system rather than a text-only classifier.



\---



\## 3. Intended Use



The system is intended for:



\- Educational demonstrations

\- Research and experimentation

\- Misinformation verification prototypes

\- Testing multimodal AI verification techniques

\- Demonstrating evidence-based AI decisions



The system is not intended to replace professional fact-checkers, journalists, scientific authorities, or other domain experts.



\---



\## 4. Input



The primary input consists of:



\- A textual claim

\- An associated image



The system also uses a curated evidence knowledge base containing factual statements and their public sources.



\---



\## 5. Output



The system produces:



\- Verification label

\- Confidence score

\- Evidence retrieved from the knowledge base

\- Source information

\- Evidence stance

\- Image-text consistency information

\- Explanation of the decision



Possible final labels are:



\- VERIFIED

\- MISINFORMATION

\- UNCERTAIN



\---



\## 6. Model Components



\### Text Encoder



Model:



`distilbert-base-uncased`



Purpose:



Convert textual claims into numerical representations for downstream analysis.



\### Image Encoder



Model:



`ViT-B-32 / OpenCLIP`



Purpose:



Convert input images into visual embeddings.



\### Evidence Encoder



Model:



Sentence Transformer embedding model.



Purpose:



Represent evidence statements as vectors for semantic retrieval.



\### Evidence Retriever



Technology:



FAISS



Purpose:



Efficiently retrieve semantically relevant evidence from the evidence knowledge base.



\### NLI Component



Model:



`nli-deberta-v3-small`



Purpose:



Determine whether retrieved evidence supports or contradicts the claim.



\### Visual Topic Analyzer



Technology:



OpenCLIP zero-shot classification.



Purpose:



Identify broad visual topics such as Earth, Moon, boiling water, red sports cars, and industrial pollution.



\### Visual Consistency Checker



Purpose:



Compare the expected topic of a claim with the detected visual topic.



\### Claim Decomposer



Purpose:



Split compound claims into independently evaluated subclaims.



\### Multimodal Fusion



Purpose:



Combine evidence, NLI, and visual consistency signals.



\### Verifier



Purpose:



Convert the combined signals into the final verification label and confidence.



\### Explanation Module



Purpose:



Generate an understandable explanation based on the signals used by the verifier.



\---



\## 7. Decision Categories



\### VERIFIED



Returned when available evidence supports the claim and the image does not create a significant contradiction.



\### MISINFORMATION



Returned when strong evidence contradicts the claim.



\### UNCERTAIN



Returned when the available evidence or visual information is insufficient, ambiguous, or inconsistent for a reliable conclusion.



\---



\## 8. Evaluation Summary



The system was evaluated using controlled and realistic validation datasets.



Controlled validation:



\- Accuracy: 86.67%

\- Macro F1: 87.50%

\- Cases: 15



Realistic multimodal validation:



\- Accuracy: 100%

\- Macro F1: 100%

\- Cases: 20



The 100% result applies only to the designed 20-case realistic validation dataset and must not be interpreted as universal real-world accuracy.



\---



\## 9. Baseline Comparison



Controlled validation results:



| System | Accuracy | Macro F1 |

|---|---:|---:|

| Evidence-only | 60.00% | 65.71% |

| Image-only | 53.33% | 23.19% |

| Full multimodal | 86.67% | 87.50% |



The full multimodal system substantially outperformed the individual evidence-only and image-only baselines on the controlled dataset.



\---



\## 10. Modality Ablation



Controlled ablation results:



| Configuration | Accuracy | Macro F1 |

|---|---:|---:|

| Evidence-only | 60.00% | 65.71% |

| Image-only | 53.33% | 23.19% |

| Evidence + Image Consistency | 86.67% | 87.50% |

| Full Multimodal | 86.67% | 87.50% |



Adding image-text consistency to evidence-based verification improved performance on the controlled dataset.



The full multimodal configuration produced the same result as evidence plus image consistency on this particular evaluation set. This does not prove that every individual component will always improve performance on every dataset.



\---



\## 11. Failure Analysis



Failure analysis was performed during development.



Important failure modes included:



\- Insufficient evidence coverage

\- Compound claims containing both supported and unsupported subclaims

\- Image and claim topic mismatch

\- Weak evidence

\- Ambiguous visual information



These failures led to improvements in:



\- Evidence coverage

\- Compound claim decomposition

\- Visual consistency analysis

\- Contradiction handling

\- Confidence-aware decisions



\---



\## 12. Known Limitations



The system has several important limitations:



1\. The evidence knowledge base covers a limited number of topics.

2\. Claims outside the available evidence may result in `UNCERTAIN`.

3\. Visual topic analysis currently focuses on supported broad topics.

4\. CLIP-based visual reasoning does not establish factual truth by itself.

5\. Controlled datasets are relatively small.

6\. Real-world misinformation can be more complex than the validation cases.

7\. Confidence scores should not be interpreted as guaranteed probabilities of truth.

8\. Public evidence sources can change over time.



\---



\## 13. Safety Considerations



The system should be treated as a decision-support tool.



Users should verify important claims against authoritative sources.



The system should not be used as the sole basis for:



\- Medical decisions

\- Legal decisions

\- Financial decisions

\- Emergency decisions

\- Decisions affecting a person's rights or safety



The `UNCERTAIN` category is intentionally provided to avoid forcing unsupported conclusions.



\---



\## 14. Privacy Considerations



The core system does not require personal information.



User-provided images and claims should be processed only for the intended verification purpose.



Sensitive or personally identifiable information should not be included in validation datasets unless appropriate authorization exists.



\---



\## 15. Reproducibility



The project provides:



\- Version-controlled source code

\- Requirements file

\- Validation datasets

\- Evaluation scripts

\- Evaluation result files

\- Unit tests

\- CI workflow

\- Architecture documentation

\- Dataset documentation

\- Failure analysis

\- Acceptance criteria



These artifacts allow another developer to reproduce the main experiments and inspect the system design.



\---



\## 16. Model Selection Rationale



The selected models were chosen to provide a practical multimodal prototype using commonly available open-source technologies.



DistilBERT provides efficient text representation.



OpenCLIP/ViT-B-32 provides image representation and zero-shot visual topic analysis.



Sentence Transformers provide semantic evidence representations.



FAISS provides efficient vector retrieval.



The NLI model provides an additional semantic check between claims and retrieved evidence.



\---



\## 17. Intended Interpretation of Results



Evaluation results demonstrate the behavior of this implementation on the documented datasets.



They should not be interpreted as evidence that the system can detect all misinformation on the internet.



Performance depends on:



\- Evidence coverage

\- Image quality

\- Claim complexity

\- Model behavior

\- Retrieval quality

\- Source quality

\- Domain



For important real-world decisions, retrieved sources and system explanations should be independently reviewed.



\---



\## 18. System Status



Current status:



Prototype suitable for academic demonstration, experimentation, and evaluation.



The system demonstrates:



\- Multimodal processing

\- Evidence retrieval

\- Source citations

\- NLI-based stance analysis

\- Image-text consistency

\- Multimodal fusion

\- Confidence-aware output

\- Explainability

\- Robustness testing

\- Failure analysis

\- Automated testing

