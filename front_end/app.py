import sys
import os

# Add parent folder (floatchat) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from backend import query_postgres, query_chroma
from utils.visualization import plot_time_series, plot_float_map

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="FloatChat 🌊", page_icon="🌐", layout="wide")

# Load CSS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------
# Sidebar
# --------------------------
st.sidebar.title("⚓ Navigation")
page = st.sidebar.radio("Go to:", ["Chat", "About"])

# --------------------------
# Chat Page
# --------------------------
if page == "Chat":
    st.markdown("<h1 class='title'>🌊 FloatChat - Ocean Data Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>💬 Chat with ARGO Data</h2>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    # Chat container
    chat_container = st.container()

    # Floating input container
    input_container = st.container()
    with input_container:
        user_input = st.text_input("", key="chat_input", placeholder="Ask something about ocean data...", label_visibility="collapsed")

    if user_input:
        # Append user message
        st.session_state.history.append({"text": user_input, "is_user": True})

        with st.spinner("🌀 AI is thinking..."):
            # Query backend
            postgres_result = query_postgres(user_input)
            chroma_result = query_chroma(user_input)
            ai_response = f"**Postgres Result:** {postgres_result}\n\n**Chroma Result:** {chroma_result}"

        # Append AI response with visualization flag
        st.session_state.history.append({"text": ai_response, "is_user": False, "visualize": True})

    # Display chat with inline visualizations
    with chat_container:
        for chat in st.session_state.history:
            bubble_class = "user-bubble" if chat["is_user"] else "ai-bubble"
            st.markdown(f"<div class='{bubble_class}'>{chat['text']}</div>", unsafe_allow_html=True)

            # Inline visualizations
            if not chat["is_user"] and chat.get("visualize"):
                try:
                    float_data = query_postgres("SELECT lat, lon, pres_mean FROM argo_profiles LIMIT 500")
                    if not isinstance(float_data, str):
                        df = pd.DataFrame(float_data, columns=["lat", "lon", "pres_mean"])
                        st.subheader("🌍 Float Map")
                        st.plotly_chart(plot_float_map(df, tooltip_col="pres_mean"), use_container_width=True)
                        st.subheader("📈 Pressure Time-series")
                        st.plotly_chart(plot_time_series(df, y_column="pres_mean", title="Pressure Time-series"), use_container_width=True)
                except Exception as e:
                    st.error(f"Visualization error: {e}")

    # Auto-scroll to latest message
    st.markdown("""
    <script>
    window.scrollTo(0, document.body.scrollHeight);
    </script>
    """, unsafe_allow_html=True)


# --------------------------
# About Page
# --------------------------
else:
    st.markdown("<h1 class='title'>ℹ️ About FloatChat</h1>", unsafe_allow_html=True)
    st.markdown("""
FloatChat is an **AI-powered chatbot** for exploring ARGO float oceanographic data.

- Built with: Streamlit, PostgreSQL, ChromaDB, RAG
- Visualizations: Plotly, Leaflet
- Fully interactive chat with session history and floating input
- Ocean-inspired UI 🌊
""")