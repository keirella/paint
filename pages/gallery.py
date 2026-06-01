import streamlit as st
import io

st.set_page_config(page_title="Gallery Studio", page_icon="🖼️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first on the main page.")
    st.stop()

st.title("🖼️ Artwork Gallery Showcase")

if "gallery" not in st.session_state or len(st.session_state.gallery) == 0:
    st.info("No drawings saved yet. Go back to Home / Canvas and draw amazing pieces!")
else:
    g_cols = st.columns(3)
    for idx, item in enumerate(st.session_state.gallery):
        with g_cols[idx % 3]:
            st.subheader(item["title"])
            st.image(item["image"], use_container_width=True)
            
            buf = io.BytesIO()
            item["image"].save(buf, format="PNG")
            byte_data = buf.getvalue()
            
            st.download_button(
                label=f"Download {item['title']}",
                data=byte_data,
                file_name=f"{item['title']}.png",
                mime="image/png",
                key=f"dl_{idx}"
            )
            st.markdown("---")

    if st.button("Clear Gallery Storage", type="primary"):
        st.session_state.gallery = []
        st.rerun()