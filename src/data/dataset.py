"""
Dataset utilities for the Multimodal Misinformation Verification project.

This module provides basic utilities for loading, validating, and splitting
multimodal claim records.
"""

from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.model_selection import train_test_split


REQUIRED_COLUMNS = [
    "claim",
    "image_path",
    "label",
]


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV dataset and validate its required columns.

    Parameters
    ----------
    file_path:
        Path to the CSV dataset.

    Returns
    -------
    pandas.DataFrame
        Loaded and validated dataset.

    Raises
    ------
    FileNotFoundError
        If the dataset file does not exist.
    ValueError
        If required columns are missing.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    if file_path.suffix.lower() != ".csv":
        raise ValueError("Currently only CSV datasets are supported.")

    dataframe = pd.read_csv(file_path)

    validate_dataset(dataframe)

    return dataframe


def validate_dataset(dataframe: pd.DataFrame) -> None:
    """
    Validate that a dataframe contains the required columns.

    Parameters
    ----------
    dataframe:
        Dataset dataframe to validate.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    if dataframe.empty:
        raise ValueError("Dataset is empty.")

    if dataframe["claim"].isna().any():
        raise ValueError("Dataset contains missing claims.")

    if dataframe["label"].isna().any():
        raise ValueError("Dataset contains missing labels.")


def split_dataset(
    dataframe: pd.DataFrame,
    test_size: float = 0.20,
    validation_size: float = 0.10,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split the dataset into training, validation, and test sets.

    Parameters
    ----------
    dataframe:
        Validated dataset.
    test_size:
        Fraction reserved for testing.
    validation_size:
        Fraction reserved for validation from the full dataset.
    random_state:
        Random seed for reproducibility.

    Returns
    -------
    tuple
        Training, validation, and test dataframes.
    """

    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    if not 0 < validation_size < 1:
        raise ValueError("validation_size must be between 0 and 1.")

    if test_size + validation_size >= 1:
        raise ValueError(
            "test_size + validation_size must be less than 1."
        )

    train_data, temp_data = train_test_split(
        dataframe,
        test_size=test_size + validation_size,
        random_state=random_state,
        stratify=dataframe["label"],
    )

    relative_validation_size = validation_size / (
        test_size + validation_size
    )

    validation_data, test_data = train_test_split(
        temp_data,
        test_size=1 - relative_validation_size,
        random_state=random_state,
        stratify=temp_data["label"],
    )

    return train_data, validation_data, test_data