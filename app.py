import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import time
import numpy as np
from PIL import Image

st.set_page_config(page_title="Web Paint", page_icon="🎨", layout="wide")

DIR = os.path.dirname(__file__)
CSS_PATH = os.path.join(DIR, "style.css")
GALLERY_DIR = os.path.join(DIR, "gallery")

if not os.path.exists(GALLERY_DIR): os.makedirs(GALLERY_DIR)

if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r") as f: css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "start"
if "drawing_mode" not in st.session_state: st.session_state.drawing_mode = "freedraw"
if "stroke_width" not in st.session_state: st.session_state.stroke_width = 5
if "stroke_color" not in st.session_state: st.session_state.stroke_color = "#000000"
if "fill_active" not in st.session_state: st.session_state.fill_active = False
if "canvas_key" not in st.session_state: st.session_state.canvas_key = "canvas_fixed"
if "canvas_data" not in st.session_state: 
    st.session_state.canvas_data = np.full((500, 800, 4), 255, dtype=np.uint8)

def apply_transform(transform_type):
    img = Image.fromarray(st.session_state.canvas_data.astype(np.uint8)).convert("RGBA")
    if transform_type == "rot":
        img = img.rotate(-90, expand=True).resize((800, 500))
    elif transform_type == "flip_h":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif transform_type == "flip_v":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    st.session_state.canvas_data = np.array(img)
    st.session_state.canvas_key = str(time.time())

def render_start_page():
    st.markdown("<div class='card-flag'></div>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        st.markdown("<h1 style='text-align:center;'>🎨 Web Paint Application</h1>", unsafe_allow_html=True)
        if st.button("Mulai Menggambar", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

def render_home_page():
    st.markdown("<div class='card-flag'></div>", unsafe_allow_html=True)
    col_tools, col_canvas = st.columns([1, 3])
    
    with col_tools:
        st.markdown("### 🛠️ Editor")
        tools = [("🖌️", "freedraw"), ("📏", "line"), ("⭕", "circle"), ("🟩", "rect")]
        c1, c2 = st.columns(2)
        for i, (label, mode) in enumerate(tools):
            target = c1 if i % 2 == 0 else c2
            if target.button(label, key=f"tool_{mode}", use_container_width=True):
                st.session_state.drawing_mode = mode
                st.rerun()
        
        st.divider()
        st.session_state.stroke_color = st.color_picker("Warna Utama", st.session_state.stroke_color)
        st.session_state.fill_active = st.checkbox("Gunakan Warna Isi (Fill)", value=st.session_state.fill_active)
        st.session_state.stroke_width = st.slider("Ukuran Brush", 1, 50, st.session_state.stroke_width)
        
        st.divider()
        st.markdown("#### Transformasi")
        t1, t2, t3 = st.columns(3)
        if t1.button("🔄 Rot", use_container_width=True): 
            apply_transform("rot")
            st.rerun()
        if t2.button("↔️ Flip H", use_container_width=True): 
            apply_transform("flip_h")
            st.rerun()
        if t3.button("↕️ Flip V", use_container_width=True): 
            apply_transform("flip_v")
            st.rerun()

    with col_canvas:
        canvas_result = st_canvas(
            fill_color=st.session_state.stroke_color if st.session_state.fill_active else "rgba(0,0,0,0)",
            stroke_width=st.session_state.stroke_width,
            stroke_color=st.session_state.stroke_color,
            height=500,
            width=800,
            drawing_mode=st.session_state.drawing_mode,
            key=st.session_state.canvas_key
        )
        
        if canvas_result.image_data is not None:
            st.session_state.canvas_data = canvas_result.image_data
            
        st.divider()
        c_save, c_gal, c_home = st.columns(3)
        if c_save.button("💾 Simpan Gambar", use_container_width=True):
            img = Image.fromarray(st.session_state.canvas_data.astype(np.uint8))
            img.save(os.path.join(GALLERY_DIR, f"Karya_{int(time.time())}.png"))
            st.toast("Tersimpan!")
        if c_gal.button("🖼️ Galeri", use_container_width=True): 
            st.session_state.page = "gallery"
            st.rerun()
        if c_home.button("🏠 Home", use_container_width=True): 
            st.session_state.page = "start"
            st.rerun()

def render_gallery_page():
    st.markdown("<h2 style='text-align:center;'>🖼️ Galeri Karya</h2>", unsafe_allow_html=True)
    files = [f for f in os.listdir(GALLERY_DIR) if f.endswith(".png")]
    if not files: st.info("Galeri kosong.")
    else:
        cols = st.columns(5)
        for i, file in enumerate(files):
            with cols[i % 5]:
                st.image(os.path.join(GALLERY_DIR, file), use_container_width=True)
                st.caption(file.replace(".png", ""))
    if st.button("⬅️ Kembali ke Editor"):
        st.session_state.page = "home"
        st.rerun()

if st.session_state.page == "start": render_start_page()
elif st.session_state.page == "home": render_home_page()
elif st.session_state.page == "gallery": render_gallery_page()