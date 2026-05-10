import streamlit as st
import pandas as pd

# Cấu hình giao diện
st.set_page_config(page_title="QuickDimension Web", page_icon="📦", layout="wide")

# CSS để làm giao diện giống dân kỹ thuật hơn
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- TỪ ĐIỂN VẬT LIỆU ---
MATERIALS = {
    "Giấy Ivory 300gsm": {"t": 0.35, "in_sd": 0.175},
    "Giấy Ivory 400gsm": {"t": 0.45, "in_sd": 0.225},
    "Giấy Duplex 350gsm": {"t": 0.45, "in_sd": 0.225},
    "Giấy Duplex 400gsm": {"t": 0.50, "in_sd": 0.25},
    "Sóng E_3 lớp": {"t": 2.0, "in_sd": 1.0},
    "Sóng B_3 lớp": {"t": 3.0, "in_sd": 1.5},
    "Sóng C_3 lớp": {"t": 4.0, "in_sd": 2.0},
    "Sóng B/E_5 lớp": {"t": 4.5, "in_sd": 2.5},
    "Sóng B/C_5 lớp": {"t": 7.0, "in_sd": 5.5},
    "Tự nhập (mm)": {"t": 0.0, "in_sd": 0.0}
}

st.title("📦 QuickDimension - Packaging Tool")
st.caption("Developed by Thanh Dat | Shyft Global - Packaging Team")

# --- SIDEBAR: INPUT ---
with st.sidebar:
    st.header("⚙️ Cấu hình đầu vào")
    
    with st.expander("1. HỘP MÀU (COLOR BOX)", expanded=True):
        input_type = st.radio("Kiểu nhập:", ["Phủ bì (OD)", "Dieline"])
        cb_mat = st.selectbox("Vật liệu Hộp màu:", list(MATERIALS.keys()), index=4)
        t_cb = MATERIALS[cb_mat]["t"]
        if cb_mat == "Tự nhập (mm)":
            t_cb = st.sidebar.number_input("Nhập độ dày (mm):", value=1.5, step=0.1)
        
        c1, c2, c3 = st.columns(3)
        l1 = c1.number_input("Dài L1", value=247.0)
        w1 = c2.number_input("Rộng W1", value=90.0)
        h1 = c3.number_input("Cao H1", value=257.0)
        
        st.markdown("---")
        st.write("**Hệ số bù (Tolerance)**")
        cidl, cidw, cidh = st.columns(3)
        cb_id_l = cidl.number_input("+ID L", value=0.0)
        cb_id_w = cidw.number_input("+ID W", value=0.0)
        cb_id_h = cidh.number_input("+ID H", value=0.0)

    with st.expander("2. INNER & MASTER LAYOUT"):
        st.subheader("Xếp Inner")
        in_mat = st.selectbox("Vật liệu Inner:", list(MATERIALS.keys()), index=5)
        t_in = MATERIALS[in_mat]["t"]
        ix, iy, iz = st.columns(3)
        in_x = ix.number_input("Trục X", value=1)
        in_y = iy.number_input("Trục Y", value=3)
        in_z = iz.number_input("Trục Z", value=1)
        
        st.subheader("Xếp Master")
        ma_mat = st.selectbox("Vật liệu Master:", list(MATERIALS.keys()), index=8)
        t_ma = MATERIALS[ma_mat]["t"]
        mx, my, mz = st.columns(3)
        ma_x = mx.number_input("Trục X", value=2, key="mx")
        ma_y = my.number_input("Trục Y", value=1, key="my")
        ma_z = mz.number_input("Trục Z", value=2, key="mz")

# --- LOGIC TÍNH TOÁN (Giữ nguyên logic của Đạt) ---
raw_cb_l = l1 + cb_id_l
raw_cb_w = w1 + cb_id_w
raw_cb_h = h1 + cb_id_h

if input_type != "Phủ bì (OD)":
    raw_cb_l += t_cb
    raw_cb_w += t_cb
    raw_cb_h += t_cb * 2

cb_L, cb_W, cb_H = max(raw_cb_l, raw_cb_w), min(raw_cb_l, raw_cb_w), raw_cb_h

# Tính Inner
id_in_l = (in_x * cb_L) + 3.0 # Giả định +3.0 ID như code gốc
id_in_w = (in_y * cb_W) + 3.0
id_in_h = (in_z * cb_H) + 0.0

in_DIE_L, in_DIE_W, in_DIE_H = id_in_l + t_in, id_in_w + t_in, id_in_h + (t_in * 2)
in_OD_L, in_OD_W, in_OD_H = id_in_l + (2*t_in) + 1.0, id_in_w + (2*t_in) + 1.0, id_in_h + (4*t_in) + 1.0

# Tính Master
id_ma_l = (ma_x * in_OD_L) + 3.0
id_ma_w = (ma_y * in_OD_W) + 3.0
id_ma_h = (ma_z * in_OD_H) + 0.0

ma_DIE_L, ma_DIE_W, ma_DIE_H = id_ma_l + t_ma, id_ma_w + t_ma, id_ma_h + (t_ma * 2)
ma_OD_L, ma_OD_W, ma_OD_H = id_ma_l + (2*t_ma) + 1.0, id_ma_w + (2*t_ma) + 1.0, id_ma_h + (4*t_ma) + 1.0

# --- HIỂN THỊ KẾT QUẢ ---
st.header("🏁 Kết quả tính toán Dieline")

res1, res2 = st.columns(2)
with res1:
    st.subheader("Inner Carton")
    st.metric("Kích thước trải L2 x W2 x H2", f"{in_DIE_L:.1f} x {in_DIE_W:.1f} x {in_DIE_H:.1f} mm")
    st.info(f"Phủ bì 1 Inner: {in_OD_L:.1f} x {in_OD_W:.1f} x {in_OD_H:.1f} mm")

with res2:
    st.subheader("Master Carton")
    st.metric("Kích thước trải L3 x W3 x H3", f"{ma_DIE_L:.1f} x {ma_DIE_W:.1f} x {ma_DIE_H:.1f} mm")
    st.info(f"Phủ bì 1 Master: {ma_OD_L:.1f} x {ma_OD_W:.1f} x {ma_OD_H:.1f} mm")

# Cảnh báo Pallet
if ma_OD_L > 1200 or ma_OD_W > 1000:
    st.warning(f"⚠ LƯU Ý: Phủ bì Master vượt khổ Pallet (1200x1000)!")

# --- XUẤT FILE SCRIPT CHO CHỊ TIỀN ---
st.markdown("---")
st.subheader("🎨 Xuất sang Adobe Illustrator")

jsx_code = f"""
// Auto-generated Script for Adobe Illustrator
var mm2pt = 2.834645;
var doc = app.documents.add();
alert("QuickDimension: Dang ve Dieline cho Dat...");
// ... logic ve hop cua Dat ...
""" # (Tại đây bạn có thể dán toàn bộ đoạn JSX script cũ vào)

st.download_button(
    label="📥 Tải Script vẽ tự động (.jsx)",
    data=jsx_code,
    file_name="Ve_Dieline_Cho_Chi_Tien.jsx",
    mime="text/javascript"
)

st.write("👉 *Hướng dẫn: Tải file trên về, mở Adobe Illustrator, chọn File -> Scripts -> Other Scripts và chọn file vừa tải.*")