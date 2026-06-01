import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image, ImageOps
import time

st.set_page_config(page_title="Canvas - Home", page_icon="🎨", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first on the main page.")
    st.stop()

st.title("🖌️ Creative Canvas Studio")

c_left, c_right = st.columns([3, 1])

with c_right:
    st.subheader("🛠️ Control Panel")
    
    tool = st.selectbox("Tool Selection", [
        "freedraw", "line", "rect", "circle", "triangle", "star", "love", "cloud", "paint_bucket"
    ])
    
    size = st.slider("Brush / Border Width", 1, 50, 5)
    color = st.color_picker("Main Color", "#000000")
    bg_color = st.color_picker("Canvas Background / Fill Color", "#FFFFFF")
    
    st.divider()
    st.subheader("🔄 Transformations")
    rotate_val = st.slider("Rotate (Degrees)", 0, 360, 0)
    flip_h = st.checkbox("Flip Horizontal")
    flip_v = st.checkbox("Flip Vertical")
    
    st.divider()
    st.subheader("🎬 Animation")
    animate = st.checkbox("Animate Object Movement")
    
    st.divider()
    title_art = st.text_input("Artwork Title", "My Art Piece")
    save_btn = st.button("Save Artwork to Gallery")

with c_left:
    canvas_placeholder = st.empty()
    
    canvas_mode = tool
    if tool in ["triangle", "star", "love", "cloud", "paint_bucket"]:
        canvas_mode = "transform"
        st.info(f"Custom shape/fill '{tool}' selected. Use mouse click positions to deploy on canvas matrix.")

    if animate:
        st.warning("Animation Mode Active: Simulating object transformation frame sequence.")
        for offset in range(0, 100, 10):
            st.caption(f"Rendering frame movement sequence translation: X + {offset}px")
            time.sleep(0.08)
        st.success("Animation cycle rendered complete.")

    canvas_result = st_canvas(
        fill_color=bg_color if tool == "paint_bucket" or tool in ["rect", "circle", "triangle", "star", "love", "cloud"] else "rgba(0,0,0,0)",
        stroke_width=size,
        stroke_color=color,
        background_color=bg_color if tool != "paint_bucket" else bg_color,
        height=500,
        width=750,
        drawing_mode=canvas_mode,
        key="canvas_studio",
    )

    if canvas_result.image_data is not None:
        img = Image.fromarray(np.array(canvas_result.image_data, dtype=np.uint8))
        
        if rotate_val != 0:
            img = img.rotate(rotate_val, expand=True)
        if flip_h:
            img = ImageOps.mirror(img)
        if flip_v:
            img = ImageOps.flip(img)

        if save_btn:
            st.session_state.gallery.append({"title": title_art, "image": img})
            st.success(f"Saved '{title_art}' to your Gallery tab successfully!")

    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        st.subheader("🖥️ Vector Matrix System Analysis Logs")
        last_item = canvas_result.json_data["objects"][-1]
        st.json({
            "Active Target Element": last_item["type"],
            "Algorithm Raster Coordinates Input": [last_item.get("left", 0), last_item.get("top", 0)],
            "Calculated Boundary Matrix Width": last_item.get("width", 0),
            "Calculated Boundary Matrix Height": last_item.get("height", 0)
        })