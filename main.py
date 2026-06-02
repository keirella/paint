# main.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image, ImageOps
import io

st.set_page_config(page_title="Ibis Paint Web", page_icon="🎨", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inisialisasi Session State
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "gallery" not in st.session_state: st.session_state.gallery = []
if "current_page" not in st.session_state: st.session_state.current_page = "login"
if "active_tool" not in st.session_state: st.session_state.active_tool = "pencil"
if "rotate_val" not in st.session_state: st.session_state.rotate_val = 0
if "flip_h" not in st.session_state: st.session_state.flip_h = False
if "flip_v" not in st.session_state: st.session_state.flip_v = False
if "show_gallery" not in st.session_state: st.session_state.show_gallery = False

# Halaman Login
if st.session_state.current_page == "login" and not st.session_state.logged_in:
    st.markdown('<div class="card-flag"></div>', unsafe_allow_html=True)
    st.markdown("<h1>🔒 Welcome to Paint Studio</h1>", unsafe_allow_html=True)
    username = st.text_input("Username", value="grafika")
    password = st.text_input("Password", type="password", value="12345")
    
    if st.button("Sign In"):
        if username == "grafika" and password == "12345":
            st.session_state.logged_in = True
            st.session_state.current_page = "home"
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# Halaman Home (Canvas)
elif st.session_state.current_page == "home" and st.session_state.logged_in:
    st.markdown("<h3 style='text-align: center;'>🎨 Paint Web Studio</h3>", unsafe_allow_html=True)
    
    t_cols = st.columns(12)
    tools = [("✏️", "pencil"), ("📏", "line"), ("⬜", "rect"), ("⚪", "circle"), 
             ("🔺", "triangle"), ("⭐", "star"), ("❤️", "love"), ("☁️", "cloud"), 
             ("🪣", "paint_bucket"), ("🔄", "rotate"), ("↔️", "flip_h"), ("↕️", "flip_v")]
    
    for i, (icon, tool_name) in enumerate(tools):
        with t_cols[i]:
            if st.button(icon, help=tool_name, use_container_width=True):
                if tool_name == "rotate": st.session_state.rotate_val = (st.session_state.rotate_val + 90) % 360
                elif tool_name == "flip_h": st.session_state.flip_h = not st.session_state.flip_h
                elif tool_name == "flip_v": st.session_state.flip_v = not st.session_state.flip_v
                else: st.session_state.active_tool = tool_name

    # Pengaturan Warna & Ukuran
    p_cols = st.columns([2, 2, 2, 6])
    with p_cols[0]: size = st.slider("Size", 1, 50, 5, label_visibility="collapsed")
    with p_cols[1]: color = st.color_picker("Main Color", "#000000", label_visibility="collapsed")
    with p_cols[2]: bg_color = st.color_picker("Bucket/Fill Color", "#FFFFFF") 

    # Canvas
    canvas_mode = "freedraw" if st.session_state.active_tool == "pencil" else \
                  ("line" if st.session_state.active_tool == "line" else \
                  ("rect" if st.session_state.active_tool == "rect" else \
                  ("circle" if st.session_state.active_tool == "circle" else "transform")))

    canvas_result = st_canvas(
        fill_color=bg_color if st.session_state.active_tool == "paint_bucket" else "rgba(0,0,0,0)",
        stroke_width=size, stroke_color=color,
        background_color=bg_color,
        height=550, width=1350,
        drawing_mode=canvas_mode, key="canvas"
    )

    # Simpan
    st.markdown("<br>", unsafe_allow_html=True)
    b_cols = st.columns(4)
    with b_cols[0]: title_art = st.text_input("Artwork Title", "My Art")
    with b_cols[1]: 
        if st.button("💾 Save to Gallery"):
            if canvas_result.image_data is not None:
                img = Image.fromarray(np.array(canvas_result.image_data, dtype=np.uint8))
                if st.session_state.rotate_val != 0: img = img.rotate(st.session_state.rotate_val, expand=True)
                if st.session_state.flip_h: img = ImageOps.mirror(img)
                if st.session_state.flip_v: img = ImageOps.flip(img)
                st.session_state.gallery.append({"title": title_art, "image": img})
                st.success("Saved!")
    with b_cols[2]:
        if st.button("🖼️ View Gallery"):
            st.session_state.show_gallery = not st.session_state.show_gallery
            st.rerun()

    # Tampilkan Galeri 
    if st.session_state.show_gallery:
        st.subheader("🖼️ Your Gallery")
        for item in st.session_state.gallery:
            st.image(item["image"], caption=item["title"])