# main.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image, ImageOps
import io
import time

st.set_page_config(page_title="Ibis Paint Web", page_icon="🎨", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "gallery" not in st.session_state:
    st.session_state.gallery = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "active_tool" not in st.session_state:
    st.session_state.active_tool = "pencil"
if "rotate_val" not in st.session_state:
    st.session_state.rotate_val = 0
if "flip_h" not in st.session_state:
    st.session_state.flip_h = False
if "flip_v" not in st.session_state:
    st.session_state.flip_v = False
if "show_gallery" not in st.session_state:
    st.session_state.show_gallery = False

if st.session_state.current_page == "login" and not st.session_state.logged_in:
    st.markdown('<div class="card-flag"></div>', unsafe_allow_html=True)
    st.markdown("<h1>🔒 Welcome to Paint Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p>Sign in to access your digital workspace</p>", unsafe_allow_html=True)
    
    username = st.text_input("Username", value="grafika")
    password = st.text_input("Password", type="password", value="12345")
    
    if st.button("Sign In"):
        if username == "grafika" and password == "12345":
            st.session_state.logged_in = True
            st.session_state.current_page = "home"
            st.rerun()
        else:
            st.error("Invalid Username or Password")

elif st.session_state.current_page == "home" and st.session_state.logged_in:
    st.markdown("<h3 style='text-align: center; margin: 0; padding: 0;'>🎨 Ibis Paint Web Studio</h3>", unsafe_allow_html=True)
    
    t_col1, t_col2, t_col3, t_col4, t_col5, t_col6, t_col7, t_col8, t_col9, t_col10, t_col11, t_col12 = st.columns(12)
    with t_col1:
        if st.button("✏️\nPencil", use_container_width=True, type="primary" if st.session_state.active_tool == "pencil" else "secondary"):
            st.session_state.active_tool = "pencil"
            st.rerun()
    with t_col2:
        if st.button("📏\nLine", use_container_width=True, type="primary" if st.session_state.active_tool == "line" else "secondary"):
            st.session_state.active_tool = "line"
            st.rerun()
    with t_col3:
        if st.button("⬜\nRect", use_container_width=True, type="primary" if st.session_state.active_tool == "rect" else "secondary"):
            st.session_state.active_tool = "rect"
            st.rerun()
    with t_col4:
        if st.button("⚪\nCircle", use_container_width=True, type="primary" if st.session_state.active_tool == "circle" else "secondary"):
            st.session_state.active_tool = "circle"
            st.rerun()
    with t_col5:
        if st.button("🔺\nTri", use_container_width=True, type="primary" if st.session_state.active_tool == "triangle" else "secondary"):
            st.session_state.active_tool = "triangle"
            st.rerun()
    with t_col6:
        if st.button("⭐\nStar", use_container_width=True, type="primary" if st.session_state.active_tool == "star" else "secondary"):
            st.session_state.active_tool = "star"
            st.rerun()
    with t_col7:
        if st.button("❤️\nLove", use_container_width=True, type="primary" if st.session_state.active_tool == "love" else "secondary"):
            st.session_state.active_tool = "love"
            st.rerun()
    with t_col8:
        if st.button("☁️\nCloud", use_container_width=True, type="primary" if st.session_state.active_tool == "cloud" else "secondary"):
            st.session_state.active_tool = "cloud"
            st.rerun()
    with t_col9:
        if st.button("🪣\nBucket", use_container_width=True, type="primary" if st.session_state.active_tool == "paint_bucket" else "secondary"):
            st.session_state.active_tool = "paint_bucket"
            st.rerun()
    with t_col10:
        if st.button("🔄\nRotate", use_container_width=True):
            st.session_state.rotate_val = (st.session_state.rotate_val + 90) % 360
            st.rerun()
    with t_col11:
        if st.button("↔️\nFlip H", use_container_width=True, type="primary" if st.session_state.flip_h else "secondary"):
            st.session_state.flip_h = not st.session_state.flip_h
            st.rerun()
    with t_col12:
        if st.button("↕️\nFlip V", use_container_width=True, type="primary" if st.session_state.flip_v else "secondary"):
            st.session_state.flip_v = not st.session_state.flip_v
            st.rerun()

    p_col1, p_col2, p_col3, p_col4 = st.columns([2, 2, 2, 6])
    with p_col1:
        size = st.slider("Size", 1, 50, 5, label_visibility="collapsed")
    with p_col2:
        color = st.color_picker("Main Color", "#000000", label_visibility="collapsed")
    with p_col3:
        bg_color = st.color_picker("Fill Color", "#FFFFFF", label_visibility="collapsed")
    with p_col4:
        animate = st.checkbox("🎬 Animate Movement", value=False)

    if animate:
        st.warning("Animation Mode Active: Simulating matrix transformation sequence.")
        for offset in range(0, 60, 15):
            time.sleep(0.05)

    canvas_mode = "freedraw" if st.session_state.active_tool == "pencil" else ("line" if st.session_state.active_tool == "line" else ("rect" if st.session_state.active_tool == "rect" else ("circle" if st.session_state.active_tool == "circle" else "transform")))

    canvas_width = 1350
    canvas_height = 550

    canvas_result = st_canvas(
        fill_color=bg_color if st.session_state.active_tool == "paint_bucket" or st.session_state.active_tool in ["rect", "circle", "triangle", "star", "love", "cloud"] else "rgba(0,0,0,0)",
        stroke_width=size,
        stroke_color=color,
        background_color=bg_color if st.session_state.active_tool != "paint_bucket" else bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=canvas_mode,
        key="full_screen_canvas",
    )

    img_processed = None
    if canvas_result.image_data is not None:
        img_processed = Image.fromarray(np.array(canvas_result.image_data, dtype=np.uint8))
        if st.session_state.rotate_val != 0:
            img_processed = img_processed.rotate(st.session_state.rotate_val, expand=True)
        if st.session_state.flip_h:
            img_processed = ImageOps.mirror(img_processed)
        if st.session_state.flip_v:
            img_processed = ImageOps.flip(img_processed)

    st.markdown("<br>", unsafe_allow_html=True)
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    
    with b_col1:
        title_art = st.text_input("Artwork Title", "My Masterpiece", label_visibility="collapsed")
    with b_col2:
        if st.button("💾 Save Artwork", use_container_width=True):
            if img_processed is not None:
                st.session_state.gallery.append({"title": title_art, "image": img_processed})
                st.success(f"Saved '{title_art}' successfully!")
    with b_col3:
        if st.button("🖼️ Toggle Gallery View", use_container_width=True):
            st.session_state.show_gallery = not st.session_state.show_gallery
            st.rerun()
    with b_col4:
        if st.button("🚪 Log Out System", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.current_page = "login"
            st.rerun()

    if st.session_state.show_gallery:
        st.markdown("---")
        st.markdown("### 🖼️ Saved Gallery Workspace")
        if len(st.session_state.gallery) == 0:
            st.info("No drawings saved yet.")
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
            if st.button("Clear Gallery Storage"):
                st.session_state.gallery = []
                st.rerun()

    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        st.markdown("---")
        last_item = canvas_result.json_data["objects"][-1]
        st.json({
            "Active Target Element": last_item["type"],
            "Algorithm Raster Coordinates Input": [last_item.get("left", 0), last_item.get("top", 0)],
            "Calculated Boundary Matrix Width": last_item.get("width", 0),
            "Calculated Boundary Matrix Height": last_item.get("height", 0)
        })