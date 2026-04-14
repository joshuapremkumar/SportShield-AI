import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import pandas as pd
import plotly.express as px
import pydeck as pdk
from pathlib import Path
import time
import cv2
import numpy as np


st.set_page_config(
    page_title="SportShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"


def load_image_from_url(url: str) -> Image.Image:
    if not url:
        return None
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception:
        pass
    return None


def display_image(uploaded_file) -> Image.Image:
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    return None


def image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def base64_to_image(b64_str: str) -> Image.Image:
    if not b64_str:
        return None
    try:
        img_bytes = base64.b64decode(b64_str)
        return Image.open(BytesIO(img_bytes))
    except Exception:
        return None


def get_confidence_label(score: float, keypoints: int = 0) -> tuple:
    """Get enhanced confidence label with emoji."""
    if score > 0.85 and keypoints > 10:
        return "High 🚨", "#FF4B4B"
    elif score > 0.6 and keypoints > 5:
        return "Medium ⚠️", "#FFA500"
    else:
        return "Low ℹ️", "#4CAF50"


def check_tampering(original_path: str, matched_path: str) -> dict:
    """Check if matched image is cropped or resized version."""
    result = {"is_cropped": False, "is_resized": False, "tampering_detected": False}

    try:
        img1 = cv2.imread(original_path)
        img2 = cv2.imread(matched_path)

        if img1 is None or img2 is None:
            return result

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]

        aspect1 = w1 / h1 if h1 > 0 else 1
        aspect2 = w2 / h2 if h2 > 0 else 1

        if abs(aspect1 - aspect2) > 0.1:
            result["is_resized"] = True
            result["tampering_detected"] = True

        if (h2 < h1 * 0.5) or (w2 < w1 * 0.5):
            result["is_cropped"] = True
            result["tampering_detected"] = True

    except Exception as e:
        print(f"Tampering check error: {e}")

    return result


def call_api(endpoint: str, files=None, data=None, method="POST"):
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "POST":
            if files:
                response = requests.post(url, files=files, data=data)
            else:
                response = requests.post(url, json=data)
        else:
            response = requests.get(url, json=data) if data else requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None


def main():
    st.title("🛡️ SportShield AI")
    st.markdown("### AI-Powered Sports Media Detection & Threat Intelligence")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", ["Live Threat Feed", "Upload", "Detect", "Dashboard"]
    )

    if page == "Live Threat Feed":
        live_threat_feed_page()
    elif page == "Upload":
        upload_page()
    elif page == "Detect":
        detect_page()
    elif page == "Dashboard":
        dashboard_page()


def live_threat_feed_page():
    st.header("🚨 Live Threat Feed")
    st.markdown("Real-time unauthorized content detection alerts")

    col1, col2 = st.columns([2, 1])

    with col1:
        image_id = st.text_input("Image ID", placeholder="Enter uploaded image ID")
    with col2:
        search_keyword = st.text_input("Search", placeholder="Keyword", value="sports")

    top_k = st.slider("Results", 1, 10, 5)

    if st.button("🔍 Scan for Threats", type="primary"):
        if not image_id:
            st.error("Enter an image ID")
            return

        with st.spinner("Scanning..."):
            data = {
                "image_id": image_id,
                "search_keyword": search_keyword,
                "top_k": top_k,
            }
            result = call_api("/detect/", data=data)

            if result and result.get("results"):
                display_live_threat_feed(result)
            else:
                st.info("No threats detected")


def display_live_threat_feed(result):
    results_data = result.get("results", [])

    countries = [r.get("country", "Unknown") for r in results_data if r.get("country")]
    unique_countries = set(countries)

    st.markdown("---")

    if unique_countries:
        st.success(f"""
🌍 **Content Spread Analysis**
> Content is spreading across **{len(unique_countries)}** countries: {", ".join(unique_countries)}
        """)

    st.markdown("### 🚨 Threat Alerts")

    for idx, r in enumerate(results_data):
        similarity = r.get("similarity_score", 0)
        keypoints = r.get("matched_keypoints", 0)
        confidence_label, color = get_confidence_label(similarity, keypoints)

        country = r.get("country", "N/A")
        city = r.get("city", "")
        domain = r.get("domain", "Unknown URL")
        url = r.get("search_url", "")

        with st.container():
            st.markdown(
                f"""
<div style="padding: 15px; border-left: 4px solid {color}; background: #1a1a1a; margin: 10px 0; border-radius: 5px;">
<h4 style="margin: 0; color: {color};">⚠️ Unauthorized Usage Detected!</h4>
<p><strong>🌍 Location:</strong> {country}{f" - {city}" if city else ""}</p>
<p><strong>🔗 Source:</strong> {domain}</p>
<p><strong>📊 Similarity:</strong> {similarity * 100:.2f}%</p>
<p><strong>🧠 Confidence:</strong> {confidence_label}</p>
<p><strong>🔍 Matched Features:</strong> {keypoints} keypoints</p>
</div>
            """,
                unsafe_allow_html=True,
            )

            if r.get("annotated_image"):
                annotated = base64_to_image(r["annotated_image"])
                if annotated:
                    with st.expander(f"View Match #{idx + 1} Analysis"):
                        st.image(
                            annotated,
                            caption="🔥 Highlighted Matching Regions",
                            use_container_width=True,
                        )

            st.markdown("---")

    total_threats = len(results_data)
    high_threats = sum(1 for r in results_data if r.get("confidence") == "High")
    medium_threats = sum(1 for r in results_data if r.get("confidence") == "Medium")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Threats", total_threats)
    col2.metric("🔴 High Risk", high_threats)
    col3.metric("🟡 Medium Risk", medium_threats)
    col4.metric("🌍 Countries Affected", len(unique_countries))


def upload_page():
    st.header("Upload Image")
    st.markdown(
        "Upload a sports media image to generate its embedding for similarity matching."
    )

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Preview")
            img = Image.open(uploaded_file)
            st.image(img, caption=uploaded_file.name, use_container_width=True)

        with col2:
            st.subheader("Upload to API")
            if st.button("Upload Image", type="primary"):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }
                result = call_api("/upload/", files=files, method="POST")

                if result:
                    st.success(f"Image uploaded successfully!")
                    st.json(result)

    with st.expander("View Uploaded Images"):
        result = call_api("/upload/list", method="GET")
        if result:
            for item in result:
                st.write(
                    f"- **{item['image_id']}**: {item['filename']} ({item['size']} bytes)"
                )


def detect_page():
    st.header("Detect Matches")
    st.markdown(
        "Search for similar images across the web using AI-powered similarity matching with explainability."
    )

    col1, col2 = st.columns(2)

    with col1:
        image_id = st.text_input(
            "Image ID", placeholder="Enter uploaded image ID (e.g., img_abc123)"
        )

    with col2:
        search_keyword = st.text_input(
            "Search Keyword",
            placeholder="e.g., NBA game highlights",
            value="sports event",
        )

    top_k = st.slider("Number of Results", 1, 10, 5)

    if st.button("Start Detection", type="primary"):
        if not image_id:
            st.error("Please enter an image ID")
            return

        with st.spinner("Searching for matches..."):
            data = {
                "image_id": image_id,
                "search_keyword": search_keyword,
                "top_k": top_k,
            }
            result = call_api("/detect/", data=data)

            if result and result.get("results"):
                display_results(result)
            else:
                st.warning("No matches found. Try a different search keyword.")


def display_results(result):
    st.success(f"Found {result['total_matches']} potential matches!")

    results_data = result.get("results", [])

    countries = [r.get("country", "Unknown") for r in results_data if r.get("country")]
    unique_countries = set(countries)

    if unique_countries:
        st.markdown(
            f"""
<div style="padding: 15px; background: #1a3a1a; border-radius: 5px; margin: 10px 0;">
🌍 <strong>Content is spreading across {len(unique_countries)} countries:</strong> {", ".join(unique_countries)}
</div>
        """,
            unsafe_allow_html=True,
        )

    for idx, r in enumerate(results_data):
        similarity = r.get("similarity_score", 0)
        keypoints = r.get("matched_keypoints", 0)
        confidence_label, color = get_confidence_label(similarity, keypoints)

        with st.expander(
            f"Match #{idx + 1}: {r.get('domain', 'Unknown')} - {similarity * 100:.1f}% similar"
        ):
            st.subheader("🧠 Why was this flagged?")

            col1, col2, col3 = st.columns(3)
            col1.metric("Similarity Score", f"{similarity * 100:.2f}%")
            col2.metric("Matching Features", keypoints)
            col3.metric("Confidence", confidence_label)

            if r.get("matched_image") and Path(r.get("original_image")).exists():
                tampering = check_tampering(
                    r.get("original_image"), r.get("matched_image")
                )
                if tampering["tampering_detected"]:
                    st.warning("⚠️ Tampering detected: Image may be cropped or resized!")

            st.markdown("### Location Info")
            geo_cols = st.columns(4)
            with geo_cols[0]:
                st.write(f"**Country**: {r.get('country', 'N/A')}")
            with geo_cols[1]:
                st.write(f"**City**: {r.get('city', 'N/A')}")
            with geo_cols[2]:
                st.write(f"**IP**: {r.get('ip_address', 'N/A')}")
            with geo_cols[3]:
                st.write(f"**Domain**: {r.get('domain', 'N/A')}")

            st.markdown("### Source URL")
            st.code(r.get("search_url", "N/A"))

            if r.get("annotated_image"):
                st.markdown("### 🔥 Highlighted Matching Regions")
                annotated_img = base64_to_image(r["annotated_image"])
                if annotated_img:
                    st.image(
                        annotated_img,
                        caption="Feature Match Visualization",
                        use_container_width=True,
                    )


def dashboard_page():
    st.header("Dashboard")
    st.markdown("Overview of detection results with geo-tracking visualization.")

    default_image = st.text_input(
        "Enter Image ID to view results", placeholder="Enter image ID"
    )

    if st.button("Load Results"):
        if default_image:
            result = call_api(f"/detect/results/{default_image}", method="GET")

            if result and result.get("results"):
                display_dashboard(result)
            else:
                st.warning("No results found for this image.")
        else:
            st.error("Please enter an image ID")


def display_dashboard(result):
    results_data = result.get("results", [])

    st.subheader("Similarity Distribution")
    if results_data:
        df = pd.DataFrame(
            [
                {
                    "Domain": r.get("domain", "Unknown"),
                    "Similarity": r.get("similarity_score", 0),
                    "Matched Keypoints": r.get("matched_keypoints", 0),
                    "Confidence": r.get("confidence", "Unknown"),
                    "Country": r.get("country", "Unknown"),
                    "City": r.get("city", "Unknown"),
                    "Latitude": r.get("latitude"),
                    "Longitude": r.get("longitude"),
                }
                for r in results_data
            ]
        )

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                df,
                x="Domain",
                y="Similarity",
                title="Similarity Scores by Source",
                color="Similarity",
                color_continuous_scale="RdYlGn",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.bar(
                df,
                x="Domain",
                y="Matched Keypoints",
                title="Matched Keypoints by Source",
                color="Matched Keypoints",
            )
            st.plotly_chart(fig2, use_container_width=True)

        countries = df[df["Country"].notna()]["Country"].unique()
        if len(countries) > 0:
            st.markdown(
                f"""
<div style="padding: 15px; background: #1a3a1a; border-radius: 5px;">
🌍 <strong>Spread Narrative:</strong> Content detected across {len(countries)} countries - {", ".join(countries)}
</div>
            """,
                unsafe_allow_html=True,
            )

        st.subheader("Geo Location Map")
        geo_df = df[df["Latitude"].notna() & df["Longitude"].notna()]

        if not geo_df.empty:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=pdk.ViewState(
                        latitude=geo_df["Latitude"].mean(),
                        longitude=geo_df["Longitude"].mean(),
                        zoom=1,
                        pitch=40,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=geo_df,
                            get_position="[Longitude, Latitude]",
                            get_color="[200, 30, 0, 160]",
                            get_radius=100000,
                            pickable=True,
                            auto_highlight=True,
                        )
                    ],
                    tooltip={
                        "text": "{Country} - {City}\nSimilarity: {Similarity:.2%}"
                    },
                )
            )
        else:
            st.info("No geo location data available")

        st.subheader("Results Table")
        st.dataframe(
            df[
                [
                    "Domain",
                    "Similarity",
                    "Matched Keypoints",
                    "Confidence",
                    "Country",
                    "City",
                ]
            ],
            use_container_width=True,
        )

    else:
        st.info("No detection results to display")


if __name__ == "__main__":
    main()
