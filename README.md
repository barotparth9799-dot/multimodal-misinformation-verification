\# Multimodal Misinformation Verification



\## Project Overview



A multimodal AI system for verifying potentially misleading information by combining text analysis, image-text consistency analysis, semantic evidence retrieval, evidence stance detection, multimodal fusion, and explainable verification.



The system accepts a textual claim and an associated image, analyzes both modalities, retrieves relevant evidence from a trusted evidence dataset, checks whether the evidence supports or contradicts the claim, and produces a final verification result.



\## Project Type



T.Y. B.Sc. Artificial Intelligence - Semester V Capstone Project



\## Problem Statement



Misinformation can contain misleading textual claims, misleading images, or a mismatch between text and visual content.



A verification system should therefore consider multiple signals instead of relying only on text classification.



This project develops a multimodal verification pipeline that combines:



\- Text representation

\- Image representation

\- Text-image consistency

\- Semantic evidence retrieval

\- Evidence stance analysis

\- Multimodal fusion

\- Confidence-aware verification

\- Human-readable explanations



\## Core Components



\### 1. Text Processing



The system cleans and validates the submitted claim before processing it.



\### 2. Text Encoding



DistilBERT is used to generate semantic representations of the claim.



\### 3. Image Encoding



OpenCLIP is used to represent images and text in a shared multimodal embedding space.



\### 4. Text-Image Consistency



The system measures how well the submitted image matches the claim.



A contrastive consistency approach compares the claim against the image and an unrelated negative description.



\### 5. Evidence Retrieval



A curated evidence dataset contains factual statements from sources such as NASA, WHO, IBM, NOAA, NIST, UNESCO, and Britannica.



Sentence Transformers are used to generate evidence embeddings, and FAISS is used for semantic similarity search.



\### 6. Evidence Stance Analysis



A Natural Language Inference model analyzes the relationship between the claim and retrieved evidence.



Evidence can be interpreted as:



\- SUPPORTS

\- CONTRADICTS

\- NEUTRAL



Bidirectional NLI analysis is used to improve contradiction detection.



\### 7. Multimodal Fusion



Evidence relevance and text-image consistency are combined to produce a final multimodal score.



A consistency gate reduces the influence of evidence when the image is poorly aligned with the claim.



\### 8. Verification



The system produces one of three outcomes:



\- VERIFIED

\- MISINFORMATION

\- UNCERTAIN



The system also produces a confidence score.



\### 9. Explanation



The final result includes a human-readable explanation describing:



\- Text signal

\- Image signal

\- Text-image consistency

\- Evidence relevance

\- Evidence stance

\- Top retrieved source



\### 10. Streamlit Interface



A Streamlit web interface allows the user to:



1\. Enter a claim

2\. Upload an image

3\. Run verification

4\. View the final result

5\. View confidence and multimodal scores

6\. Read the generated explanation

7\. Inspect retrieved evidence and source links



\## Technology Stack



\- Python

\- PyTorch

\- Hugging Face Transformers

\- Sentence Transformers

\- OpenCLIP

\- OpenCV

\- FAISS

\- Scikit-learn

\- Streamlit

\- Git



\## Project Structure



```text

multimodal\_misinformation/

│

├── app/

│   └── streamlit\_app.py

│

├── configs/

│   └── config.py

│

├── data/

│   ├── evidence/

│   │   └── evidence.csv

│   └── processed/

│       └── evaluation\_results.txt

│

├── sample\_media/

│   ├── climate\_test.png

│   ├── test 2.png

│   ├── earth\_test.jpg

│   ├── moon\_test.jpg

│   └── boiling\_water\_test.jpg

│

├── src/

│   ├── data/

│   ├── evaluation/

│   ├── explanation/

│   ├── image/

│   ├── multimodal/

│   ├── retrieval/

│   ├── text/

│   └── verification/

│

├── tests/

├── Dockerfile

├── README.md

└── requirements.txt

