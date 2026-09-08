\# Multimodal Misinformation Verification System

\# Architecture and Design



\## 1. System Overview



The system verifies a user-provided claim using three main sources of information:



1\. Textual information from the claim.

2\. Visual information from the associated image.

3\. External factual evidence stored in the evidence knowledge base.



The system combines these signals using multimodal consistency analysis, evidence retrieval, natural language inference, and confidence-aware decision logic.



The final result is one of three labels:



\- VERIFIED

\- MISINFORMATION

\- UNCERTAIN



The system also provides confidence, retrieved evidence, source information, and a human-readable explanation.



\## 2. High-Level Architecture



```text

User

&#x20;|

&#x20;| Claim + Image

&#x20;v

Streamlit User Interface

&#x20;|

&#x20;v

Multimodal Verification Pipeline

&#x20;|

&#x20;+--------------------+----------------------+

&#x20;|                    |                      |

&#x20;v                    v                      v

Text Processing    Image Processing     Evidence Retrieval

&#x20;|                    |                      |

&#x20;v                    v                      v

Text Encoder       Image Encoder       Evidence Encoder

&#x20;|                    |                      |

&#x20;|                    v                      v

&#x20;|              Visual Topic Analysis    FAISS Index

&#x20;|                    |                      |

&#x20;|                    v                      v

&#x20;|              Image-Text Consistency   Top-K Evidence

&#x20;|                                           |

&#x20;|                                           v

&#x20;|                                    NLI Stance Analysis

&#x20;|                                           |

&#x20;+--------------------+----------------------+

&#x20;                     |

&#x20;                     v

&#x20;             Multimodal Fusion

&#x20;                     |

&#x20;                     v

&#x20;            Verification Decision

&#x20;                     |

&#x20;         +-----------+-----------+

&#x20;         |                       |

&#x20;         v                       v

&#x20;  Explanation Generator    Confidence Score

&#x20;         |                       |

&#x20;         +-----------+-----------+

&#x20;                     |

&#x20;                     v

&#x20;              Final Result

