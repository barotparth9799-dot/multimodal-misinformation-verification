"""
Central configuration for the Multimodal Misinformation Verification project.
"""

from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EVIDENCE_DATA_DIR = DATA_DIR / "evidence"
METADATA_DIR = DATA_DIR / "metadata"

MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"


# ============================================================
# MODEL CONFIGURATION
# ============================================================

TEXT_MODEL_NAME = "distilbert-base-uncased"

IMAGE_TEXT_MODEL_NAME = "ViT-B-32"
IMAGE_TEXT_PRETRAINED = "openai"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# DATA CONFIGURATION
# ============================================================

RANDOM_SEED = 42

TEST_SIZE = 0.20
VALIDATION_SIZE = 0.10

NUM_CLASSES = 2

CLASS_NAMES = {
    0: "Real",
    1: "Misinformation"
}


# ============================================================
# MULTIMODAL CONFIGURATION
# ============================================================

TEXT_EMBEDDING_DIM = 768
IMAGE_EMBEDDING_DIM = 512

FUSION_HIDDEN_DIM = 256

DROPOUT = 0.30


# ============================================================
# EVIDENCE RETRIEVAL CONFIGURATION
# ============================================================

TOP_K_EVIDENCE = 5

SIMILARITY_THRESHOLD = 0.50


# ============================================================
# VERIFICATION CONFIGURATION
# ============================================================

CONFIDENCE_THRESHOLD = 0.70


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_TITLE = "Multimodal Misinformation Verification"

APP_DESCRIPTION = (
    "AI-assisted verification using text analysis, "
    "image-text consistency, multimodal fusion, "
    "and semantic evidence retrieval."
)


# ============================================================
# DEVICE CONFIGURATION
# ============================================================

DEVICE = "cpu"


# ============================================================
# REPRODUCIBILITY
# ============================================================

SEED = RANDOM_SEED