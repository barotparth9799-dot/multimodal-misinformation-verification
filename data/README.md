\# Data Directory



This directory contains the datasets and supporting data used by the

Multimodal Misinformation Verification project.



\## Directory Structure



\- `raw/` - Original datasets downloaded or collected for the project.

\- `processed/` - Cleaned and preprocessed data used by the models.

\- `evidence/` - Retrieved or stored evidence documents used for verification.

\- `metadata/` - Metadata associated with claims, images, and evidence.



\## Data Handling



Original raw data should not be modified directly.



All preprocessing operations should create outputs in the `processed/`

directory so that the original data remains available for reproducibility.



\## Privacy and Security



Do not store passwords, API keys, private personal information, or other

sensitive information in this directory.



Large datasets and model files are excluded from Git using `.gitignore`.



\## Project Use



The data will support:



1\. Text-based misinformation analysis.

2\. Image-text consistency analysis.

3\. Multimodal feature fusion.

4\. Evidence retrieval.

5\. Verification and classification.

6\. Evaluation and error analysis.

