\# Dataset and Data Governance Documentation



\## 1. Purpose



This project uses two types of data:



1\. A public evidence knowledge base containing factual statements and their source organizations.

2\. Controlled validation datasets containing text claims and associated images used to evaluate the multimodal verification system.



The project does not rely on private personal data.



\---



\## 2. Evidence Knowledge Base



The evidence knowledge base is stored in:



`data/evidence/evidence.csv`



Each evidence record contains:



| Field | Description |

|---|---|

| evidence\_id | Unique identifier for the evidence record |

| text | Factual statement used for verification |

| source | Organization or publisher associated with the evidence |

| url | Public source URL |



\### Current Evidence Records



The knowledge base contains evidence from public and authoritative organizations including:



\- NASA

\- WHO

\- NIST

\- NOAA

\- UNESCO

\- IBM

\- Britannica



Examples include information about:



\- Earth and the Moon

\- Climate change

\- Vaccination

\- Physical activity

\- Water boiling temperature

\- Photosynthesis

\- Pacific Ocean

\- Artificial intelligence

\- Misinformation



NASA evidence was also added for Moon size and Moon composition to improve coverage of realistic Moon-related claims.



\---



\## 3. Evidence Source Policy



Evidence is selected from publicly available sources that are suitable for factual verification.



Priority is given to:



1\. Government and scientific organizations

2\. International organizations

3\. Established educational/reference organizations

4\. Other reputable public sources when required



The system stores the source organization and URL with each evidence record so that retrieved evidence can be traced back to its source.



\---



\## 4. Validation Dataset



The project contains controlled validation datasets under:



`experiments/`



The main realistic validation dataset is:



`experiments/realistic\_validation\_dataset.csv`



It contains 20 test cases covering different combinations of claims and images.



The cases include:



\- Supported factual claims

\- False claims

\- Matched claim-image pairs

\- Mismatched claim-image pairs

\- Ambiguous visual situations

\- Compound claims

\- Claims with weak or missing evidence

\- Strongly contradictory claims



The validation dataset is designed to test the complete multimodal pipeline rather than only text classification.



\---



\## 5. Validation Labels



The system uses three final verification categories:



| Label | Meaning |

|---|---|

| VERIFIED | Available evidence supports the claim and there is no significant visual contradiction |

| MISINFORMATION | Evidence strongly contradicts the claim |

| UNCERTAIN | Evidence or visual information is insufficient, ambiguous, or inconsistent for a confident decision |



The `UNCERTAIN` category is important because the system should not force a binary true/false decision when the available information is insufficient.



\---



\## 6. Image Data



Images used during validation represent topics such as:



\- Earth

\- Moon

\- Boiling water

\- Red sports car

\- Industrial pollution



The image analysis component uses OpenCLIP/ViT-B-32 embeddings together with visual topic analysis.



Images are used to test whether the visual content is consistent with the textual claim.



A visually unrelated image can therefore reduce confidence or produce an `UNCERTAIN` result even when the text itself has supporting evidence.



\---



\## 7. Data Dictionary



\### Evidence Dataset



| Column | Type | Description |

|---|---|---|

| evidence\_id | String | Unique evidence identifier |

| text | String | Factual evidence statement |

| source | String | Evidence source organization |

| url | String | Public source URL |



\### Realistic Validation Dataset



| Field | Type | Description |

|---|---|---|

| case\_id | String | Unique validation case identifier |

| claim | String | Text claim submitted to the system |

| image | String | Associated validation image |

| expected\_label | String | Expected verification category |

| category | String | Test scenario/category |



\### Validation Results



The result files contain model outputs such as:



\- Predicted label

\- Confidence

\- Verification scores

\- Evidence information

\- Visual consistency information

\- NLI stance

\- Explanation



\---



\## 8. Data Splitting and Leakage Considerations



This project primarily evaluates a verification pipeline rather than training a new supervised classifier on the validation cases.



The controlled validation cases are kept separate from the evidence knowledge base evaluation process as much as practical.



The validation cases are used for testing and are not treated as training examples.



No validation result is used to modify the expected label after seeing the model prediction.



When changes are made to the evidence knowledge base or verification logic, validation is rerun to measure the effect of the change.



\---



\## 9. Reproducibility



The project records the important software and model configuration in the repository.



The environment uses:



\- Python 3.11.9

\- PyTorch

\- Transformers

\- Sentence Transformers

\- Scikit-learn

\- OpenCV

\- Streamlit

\- FAISS

\- OpenCLIP



Model configuration includes:



\- DistilBERT for text encoding

\- ViT-B-32/OpenCLIP for image encoding

\- Sentence Transformer embeddings for evidence retrieval

\- NLI model for evidence stance analysis



Dependencies are recorded in:



`requirements.txt`



The project structure and configuration files are version controlled with Git.



\---



\## 10. Ethical and Privacy Considerations



The system is designed around public factual evidence and does not require personal user information for its core verification process.



The validation images are used for technical evaluation and are not intended to identify individuals.



The project should avoid using private, sensitive, copyrighted, or personally identifiable data unless appropriate permission and legal rights are available.



Public source URLs are retained to improve transparency and traceability.



\---



\## 11. Data Versioning



Changes to datasets and evidence records are tracked through Git commits.



Important changes include:



\- Initial evidence knowledge base

\- Addition of Moon-related evidence

\- Validation dataset development

\- Realistic validation improvements

\- Failure-analysis-driven evidence coverage improvements



This allows the project to identify which version of the data was used during evaluation.



\---



\## 12. Annotation and Test Case Design



Validation cases are manually designed according to their intended verification outcome.



Each case specifies:



1\. A textual claim

2\. An associated image

3\. An expected verification category

4\. A test scenario



The cases intentionally include both easy and difficult situations so that evaluation is not based only on simple matched examples.



Special attention is given to:



\- Compound claims

\- Contradictory evidence

\- Missing evidence

\- Visual mismatch

\- Uncertain decisions

\- False-positive risk

\- False-negative risk



\---



\## 13. Data Quality Controls



Before validation, the project checks:



\- Required dataset fields

\- Valid image paths

\- Non-empty claims

\- Valid expected labels

\- Evidence source information

\- Evidence URLs

\- Consistent case identifiers



Validation results are reviewed using accuracy, Macro F1, confusion matrix, confidence calibration, modality ablation, robustness testing, and failure analysis.



\---



\## 14. Known Data Limitations



The validation dataset is controlled and relatively small.



Therefore:



\- A high validation score does not prove universal real-world accuracy.

\- The evidence knowledge base covers only selected factual topics.

\- Visual topic analysis is limited to supported topics.

\- Novel claims outside the evidence coverage may produce `UNCERTAIN`.

\- Results may change when new evidence sources or topics are added.



The 20-case realistic validation result should therefore be reported as evidence of system functionality, not as proof of unrestricted real-world misinformation detection.



\---



\## 15. Reproducibility Checklist



Before reproducing the evaluation:



1\. Use the project repository.

2\. Create the documented Python environment.

3\. Install dependencies from `requirements.txt`.

4\. Ensure the evidence CSV is available.

5\. Ensure validation images are available.

6\. Run the validation scripts.

7\. Record the resulting metrics.

8\. Compare results with the committed evaluation artifacts.



\---



\## 16. Governance Summary



The project follows these principles:



\- Use traceable public evidence.

\- Keep validation data separate from training logic.

\- Record dataset changes through version control.

\- Avoid unnecessary personal data.

\- Report uncertainty instead of forcing unsupported decisions.

\- Preserve source citations.

\- Document limitations.

\- Make experiments reproducible.

\- Do not present controlled validation performance as universal real-world accuracy.

