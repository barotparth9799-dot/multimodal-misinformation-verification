"""
Streamlit user interface for the Multimodal Misinformation
Verification project.
"""

import sys
import tempfile
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.pipeline import create_pipeline


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Multimodal Misinformation Verification",
    page_icon="🔎",
    layout="wide",
)


# ---------------------------------------------------------
# Load and cache the AI pipeline
# ---------------------------------------------------------

@st.cache_resource
def load_pipeline():
    """
    Load and cache the multimodal verification pipeline.

    Caching prevents the AI models from being loaded again
    every time the user interacts with the Streamlit page.
    """

    return create_pipeline()


# ---------------------------------------------------------
# Application title
# ---------------------------------------------------------

st.title("🔎 Multimodal Misinformation Verification")

st.write(
    "Enter a claim and upload an associated image to "
    "analyze the claim using multimodal AI."
)


# ---------------------------------------------------------
# Claim input
# ---------------------------------------------------------

st.subheader("Claim")

claim = st.text_area(
    "Enter the claim you want to verify:",
    placeholder=(
        "Example: Climate change is mainly caused "
        "by human activities."
    ),
    height=120,
)


# ---------------------------------------------------------
# Image input
# ---------------------------------------------------------

st.subheader("Image")

uploaded_image = st.file_uploader(
    "Upload an image associated with the claim:",
    type=["jpg", "jpeg", "png"],
)


if uploaded_image is not None:

    st.image(
        uploaded_image,
        caption="Uploaded image",
        width=500,
    )


# ---------------------------------------------------------
# Verification button
# ---------------------------------------------------------

verify_button = st.button(
    "🔍 Verify Claim",
    type="primary",
)


if verify_button:

    # -----------------------------------------------------
    # Validate claim
    # -----------------------------------------------------

    if not claim.strip():

        st.warning(
            "Please enter a claim before starting verification."
        )

    # -----------------------------------------------------
    # Validate image
    # -----------------------------------------------------

    elif uploaded_image is None:

        st.warning(
            "Please upload an image before starting verification."
        )

    else:

        try:

            # -------------------------------------------------
            # Load pipeline
            # -------------------------------------------------

            with st.spinner(
                "Loading multimodal AI models..."
            ):

                pipeline = load_pipeline()


            # -------------------------------------------------
            # Save uploaded image temporarily
            # -------------------------------------------------

            suffix = Path(
                uploaded_image.name
            ).suffix.lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temporary_file:

                temporary_file.write(
                    uploaded_image.getbuffer()
                )

                temporary_image_path = (
                    temporary_file.name
                )


            # -------------------------------------------------
            # Run verification
            # -------------------------------------------------

            with st.spinner(
                "Analyzing claim, image, consistency, "
                "and retrieved evidence..."
            ):

                result = pipeline.verify(
                    claim=claim,
                    image_path=temporary_image_path,
                )


            # -------------------------------------------------
            # Verification result
            # -------------------------------------------------

            st.divider()

            st.subheader("Verification Result")

            result_col1, result_col2 = st.columns(2)


            with result_col1:

                if result["label"] == "VERIFIED":

                    st.success(
                        f"✅ {result['label']}"
                    )

                elif result["label"] == "MISINFORMATION":

                    st.error(
                        f"⚠️ {result['label']}"
                    )

                else:

                    st.warning(
                        f"❓ {result['label']}"
                    )


            with result_col2:

                st.metric(
                    "Confidence",
                    f"{result['confidence'] * 100:.2f}%",
                )


            # -------------------------------------------------
            # Multimodal scores
            # -------------------------------------------------

            st.subheader("Multimodal Analysis")

            score_col1, score_col2 = st.columns(2)
            score_col3, score_col4 = st.columns(2)


            with score_col1:

                st.metric(
                    "Text Score",
                    f"{result['text_score']:.4f}",
                )


            with score_col2:

                st.metric(
                    "Image Score",
                    f"{result['image_score']:.4f}",
                )


            with score_col3:

                st.metric(
                    "Text-Image Consistency",
                    f"{result['consistency_score']:.4f}",
                )


            with score_col4:

                st.metric(
                    "Evidence Score",
                    f"{result['evidence_score']:.4f}",
                )


            st.metric(
                "Final Fused Score",
                f"{result['fused_score']:.4f}",
            )


            # -------------------------------------------------
            # Explanation
            # -------------------------------------------------

            st.subheader("Explanation")

            st.info(
                result["explanation"]
            )


            # -------------------------------------------------
            # Retrieved evidence
            # -------------------------------------------------

            st.subheader(
                "Retrieved Evidence"
            )

            evidence_results = result.get(
                "evidence",
                [],
            )


            if evidence_results:

                for index, evidence in enumerate(
                    evidence_results,
                    start=1,
                ):

                    st.markdown(
                        f"**Evidence {index} — "
                        f"{evidence['evidence_id']}**"
                    )

                    st.write(
                        evidence["text"]
                    )

                    st.write(
                        f"**Similarity:** "
                        f"{evidence['similarity']:.4f}"
                    )

                    st.write(
                        f"**Source:** "
                        f"{evidence['source']}"
                    )


                    if evidence.get("url"):

                        st.markdown(
                            f"[Open source]({evidence['url']})"
                        )


                    st.divider()


            else:

                st.info(
                    "No supporting evidence was retrieved."
                )


        except Exception as error:

            st.error(
                "An error occurred while running "
                "the verification pipeline."
            )

            st.exception(error)