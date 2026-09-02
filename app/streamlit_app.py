"""
Streamlit user interface for the Multimodal Misinformation
Verification project.
"""

import streamlit as st


st.set_page_config(
    page_title="Multimodal Misinformation Verification",
    page_icon="🔎",
    layout="wide",
)


st.title("🔎 Multimodal Misinformation Verification")

st.write(
    "Enter a claim and upload an associated image to "
    "analyze the claim using multimodal AI."
)


st.subheader("Claim")

claim = st.text_area(
    "Enter the claim you want to verify:",
    placeholder="Example: Climate change is mainly caused by human activities.",
    height=120,
)


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


verify_button = st.button(
    "🔍 Verify Claim",
    type="primary",
)


if verify_button:
    if not claim.strip():
        st.warning(
            "Please enter a claim before starting verification."
        )

    elif uploaded_image is None:
        st.warning(
            "Please upload an image before starting verification."
        )

    else:
        st.success(
            "Claim and image received successfully. "
            "The verification pipeline will be connected next."
        )