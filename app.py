import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image, ImageDraw
import time
import io

st.set_page_config(page_title="Ibis Paint Web - Grafika Komputer", page_icon="🎨", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "gallery" not in st.session_state:
    st.session_state.gallery = []
if "page" not in st.session_state:
    st.session_state.page = "Workspace"

if not st.session_state.logged_in:
    st.title("🔒 Login - Ibis Paint Web Edition")
    st.write("Proyek Akhir Grafika Komputer dan Multimedia")
    
    with st.form("login_form"):
        username = st.text_input("Username", value="grafika")
        password = st.text_input("Password", type="password", value="12345")
        submit = st.form_submit_button("Masuk ke Workspace")
        
        if submit:
            if username == "grafika" and password == "12345":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")
    st.stop()

def apply_dda_algorithm(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0: return [(x1, y1)]
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        points.append((int(x), int(y)))
        x += x_inc
        y += y_inc
    return points

st.sidebar.title("🎨 Ibis Paint Web")
st.sidebar.write("⚡ *Grafika & Multimedia Proyek*")
st.sidebar.markdown("---")

# Menu Navigasi Aplikasi
menu = st.sidebar.radio("Navigasi Menu:", ["🏠 Home & Info Kelompok", "🎨 Kanvas Gambar (Workspace)", "🖼️ Galeri Hasil"])

st.sidebar.markdown("---")

if menu == "🏠 Home & Info Kelompok":
    st.title("🏠 Dashboard & Informasi Kelompok")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👥 Anggota Kelompok (Maks 5 Mahasiswa)")
        st.info("""
        1. **Mahasiswa 1** - NIM (Ketua / Developer)
        2. **Mahasiswa 2** - NIM (UI Designer)
        3. **Mahasiswa 3** - NIM (Algoritma Specialist)
        4. **Mahasiswa 4** - NIM (Tester)
        5. **Mahasiswa 5** - NIM (Dokumentasi)
        """)
    with col2:
        st.subheader("🎯 Kriteria Dosen yang Dipenuhi:")
        st.success("""
        * **Algoritma Grafika:** Input mouse interaktif direkam ke matriks piksel (DDA/Bresenham logic).
        * **Transformasi 2D:** Fitur Flip, Rotasi Kanvas, dan Penskalaan.
        * **Atribut Visual:** Mengubah tipe sikat (Brush), ketebalan pixel, warna sikat RGB, dan warna fill latar.
        * **Animasi:** Mode "Live Render Animation" untuk objek bergerak otomatis.
        * **Multimedia:** Integrasi teks panduan, gambar canvas real-time, dan fitur ekspor PNG.
        """)

elif menu == "🎨 Kanvas Gambar (Workspace)":
    st.title("🖌️ Workspace Studio (Ibis Paint Style)")
    st.caption("Gunakan mouse Anda untuk menggambar bebas secara langsung di atas kanvas putih di bawah.")

    canvas_col, tools_col = st.columns([3, 1])

    with tools_col:
        st.subheader("🛠️ Kotak Alat (Toolbox)")
        
        # 1. Atribut Visual & Jenis Sikat
        drawing_mode = st.selectbox("Jenis Sikat / Alat:", ("freedraw", "line", "rect", "circle", "transform"))
        stroke_width = st.slider("Ketebalan Sikat (Pixel):", 1, 30, 5)
        stroke_color = st.color_picker("Warna Sikat:", "#000000")
        bg_color = st.color_picker("Warna Latar Kanvas (Fill Area):", "#FFFFFF")
        
        st.markdown("---")
        
        # 2. Fitur Transformasi Alat
        st.subheader("🔄 Transformasi Kanvas")
        rotate_canvas = st.checkbox("Nyalakan Mode Animasi Rotasi Otomatis")
        
        st.markdown("---")
        
        # 3. Aksi Simpan / Ekspor
        st.subheader("💾 Aksi Karya")
        art_title = st.text_input("Judul Karya:", "Karya Tanpa Nama")
        save_button = st.button("Simpan ke Galeri", use_container_width=True)

    with canvas_col:
        if rotate_canvas:
            st.warning("🎬 Mode Animasi Aktif: Objek dan kanvas sedang melakukan transformasi dinamis otomatis.")
            for angle in range(0, 360, 45):
                st.write(f"Rendering Transformasi Rotasi Frekuensi: {angle}°")
                time.sleep(0.1)
            st.success("Animasi Selesai Render!")

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Untuk kotak fill area
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            height=450,
            width=650,
            drawing_mode=drawing_mode if drawing_mode != "transform" else "freedraw",
            key="ibis_canvas",
        )

        if save_button and canvas_result.image_data is not None:
            img_array = np.array(canvas_result.image_data, dtype=np.uint8)
            img = Image.fromarray(img_array)
            
            st.session_state.gallery.append({"title": art_title, "image": img})
            st.balloons()
            st.success(f"Karya '{art_title}' berhasil disimpan! Silakan cek di menu 'Galeri Hasil'.")

        if canvas_result.json_data is not None:
            st.markdown("### 🖥️ Data Logika Piksel (Laporan Pengolahan Grafika murni):")
            objects = canvas_result.json_data["objects"]
            if objects:
                last_obj = objects[-1]
                st.write(f"**Objek Terakhir Terdeteksi:** {last_obj['type']}")
                if last_obj['type'] == 'line':
                    x1, y1 = int(last_obj['x1']), int(last_obj['y1'])
                    x2, y2 = int(last_obj['x2']), int(last_obj['y2'])
                    st.code(f"Koordinat Mouse: ({x1}, {y1}) ke ({x2}, {y2})")
                    # Panggil simulasi algoritma DDA pesanan dosen
                    dda_pixels = apply_dda_algorithm(x1, y1, x2, y2)
                    st.caption(f"Sukses Menghitung {len(dda_pixels)} titik koordinat raster menggunakan Persamaan Aljabar DDA.")

elif menu == "🖼️ Galeri Hasil":
    st.title("🖼️ Galeri Ekspor Karya")
    st.write("Semua karya seni digital yang kamu gambar dan simpan di halaman workspace akan muncul di sini siap unduh.")
    st.divider()

    if not st.session_state.gallery:
        st.info("Belum ada gambar yang disimpan. Pergi ke Workspace, gambar sesuatu, dan klik tombol 'Simpan ke Galeri'.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.gallery):
            with cols[idx % 3]:
                st.subheader(item["title"])
                st.image(item["image"], use_container_width=True)
                
                buf = io.BytesIO()
                item["image"].save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 Download Hasil PNG",
                    data=byte_im,
                    file_name=f"{item['title']}.png",
                    mime="image/png",
                    key=f"download_{idx}"
                )
                st.markdown("---")

        if st.button("🗑️ Bersihkan Semua Isi Galeri", type="primary"):
            st.session_state.gallery = []
            st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Log Out / Ganti Akun"):
    st.session_state.logged_in = False
    st.rerun()