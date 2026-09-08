\# Sequence and C4 Design



\## 1. C4 Context View



The system is designed as a multimodal misinformation verification application.



\### External Actors



\- User

\- Evidence source organizations



\### Main System



\*\*Multimodal Misinformation Verification System\*\*



The user submits a claim and an associated image. The system processes both modalities, retrieves supporting or contradicting evidence, evaluates consistency, and produces a verification result.



\### External Information



The system uses factual evidence collected from trusted public sources such as:



\- NASA

\- WHO

\- NIST

\- NOAA

\- UNESCO

\- IBM

\- Britannica



The evidence records preserve source names and URLs for traceability.



\---



\## 2. C4 Container View



The major logical containers are:



\### User Interface



Technology: Streamlit



Responsibilities:



\- Accept claim.

\- Accept image.

\- Start verification.

\- Display result.

\- Display confidence.

\- Display evidence.

\- Display explanation.



\### Verification Pipeline



Technology: Python



Responsibilities:



\- Coordinate all verification components.

\- Manage multimodal processing.

\- Combine evidence and visual signals.

\- Produce final verification output.



\### Text Analysis Container



Main components:



\- Text processor

\- Text encoder

\- Claim decomposer



Responsibilities:



\- Clean claims.

\- Generate semantic representations.

\- Split compound claims into independently testable statements.



\### Image Analysis Container



Main components:



\- Image encoder

\- Visual topic analyzer

\- Visual consistency checker



Responsibilities:



\- Process images.

\- Identify visual topics.

\- Compare visual information with the claim.

\- Detect visual mismatch.



\### Evidence Retrieval Container



Main components:



\- Evidence encoder

\- FAISS retriever

\- Evidence knowledge base



Responsibilities:



\- Encode evidence.

\- Build/search the FAISS index.

\- Retrieve relevant factual evidence.

\- Preserve evidence source and URL.



\### Evidence Reasoning Container



Main components:



\- NLI stance analyzer

\- Multimodal fusion

\- Verification classifier

\- Explanation generator



Responsibilities:



\- Determine whether evidence supports or contradicts a claim.

\- Combine multimodal signals.

\- Produce the final label.

\- Generate an understandable explanation.



\---



\## 3. C4 Component View



```text

Multimodal Verification Pipeline

|

+-- Text Processing

|   +-- Claim Cleaning

|   +-- Text Encoder

|   +-- Claim Decomposer

|

+-- Image Processing

|   +-- Image Encoder

|   +-- Visual Topic Analyzer

|   +-- Visual Consistency Checker

|

+-- Evidence Retrieval

|   +-- Evidence Encoder

|   +-- FAISS Retriever

|   +-- Evidence CSV Knowledge Base

|

+-- Evidence Reasoning

|   +-- NLI Stance Analyzer

|   +-- Multimodal Fusion

|   +-- Verification Classifier

|   +-- Explanation Generator

|

+-- Streamlit Interface

