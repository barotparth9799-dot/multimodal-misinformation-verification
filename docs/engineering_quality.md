\# Engineering Quality and Security Checks



\## 1. Automated Testing



The project uses pytest for automated unit testing.



The test suite covers major components including:



\- Text processing

\- Text encoding

\- Image encoding

\- Visual topic analysis

\- Visual consistency

\- Evidence encoding

\- Evidence retrieval

\- Evidence stance analysis

\- Multimodal fusion

\- Verification

\- Explanation

\- Claim decomposition

\- Pipeline integration

\- Robustness and edge cases



The GitHub Actions workflow automatically runs the test suite on repository pushes and pull requests.



\---



\## 2. Source Compilation Check



Continuous integration runs:



`python -m compileall src`



This checks that Python source files can be compiled successfully before the test suite is executed.



\---



\## 3. Dependency Management



Project dependencies are recorded in:



`requirements.txt`



The project uses a dedicated Python virtual environment during local development.



Dependencies should be reviewed before release to identify:



\- Outdated packages

\- Known vulnerabilities

\- Unnecessary dependencies

\- Compatibility problems



\---



\## 4. Security and Dependency Review



Before a production release, dependency security should be checked using an appropriate vulnerability scanner.



Recommended checks include:



\- Python package vulnerability scanning

\- Dependency version review

\- Removal of unused packages

\- Review of transitive dependencies

\- Verification of trusted package sources



Security scanning is treated as a release-quality gate rather than part of the runtime verification pipeline.



\---



\## 5. Input Security



The application accepts user-provided text and images.



Important controls include:



\- Rejecting empty claims

\- Validating image paths

\- Handling unsupported image formats

\- Handling missing files

\- Limiting processing to expected application inputs

\- Avoiding execution of user-provided content



\---



\## 6. Privacy



The verification system does not require personal information for its core operation.



User-provided claims and images should not be unnecessarily stored after processing.



Validation datasets should avoid personally identifiable or sensitive information.



\---



\## 7. Reliability



The system includes handling for:



\- Missing evidence

\- Unknown visual topics

\- Weak evidence

\- Contradictory evidence

\- Image-text mismatch

\- Compound claims

\- Invalid inputs

\- Uncertain verification decisions



The `UNCERTAIN` result prevents the system from presenting an unsupported binary decision when available information is insufficient.



\---



\## 8. Code Review and Version Control



Development is performed using Git branches and commits.



Major project milestones are represented by descriptive commits.



Examples include:



\- Initial project setup

\- Dependency configuration

\- Multimodal pipeline implementation

\- Baseline comparison

\- Modality ablation

\- Failure analysis

\- Architecture documentation

\- Dataset and data governance documentation

\- Continuous integration workflow



This provides a traceable engineering history.



\---



\## 9. Release Quality Gate



Before final release, the following should be verified:



\- All automated tests pass

\- Source compilation succeeds

\- Dependencies are reviewed

\- Security checks are completed

\- Validation results are reproducible

\- Documentation is complete

\- Docker/clean-machine execution succeeds

\- Final application workflow is tested end-to-end



\---



\## 10. Engineering Evidence



The repository contains evidence for:



\- Automated unit testing

\- Continuous integration

\- Version-controlled development

\- Dependency specification

\- Robustness testing

\- Failure analysis

\- Architecture design

\- Dataset governance

\- Reproducibility

\- Security considerations

\- Release-quality checks

