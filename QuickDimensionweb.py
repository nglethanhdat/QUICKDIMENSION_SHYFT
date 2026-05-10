import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==========================================
# CẤU HÌNH TRANG WEB & GIAO DIỆN
# ==========================================
st.set_page_config(page_title="QuickDimension - Pro Web Version", page_icon="📦", layout="wide")

# Ép giao diện sáng màu để không bị chìm chữ và ép font Monospace cho phần tính toán
st.markdown("""
    <style>
    /* Tổng thể nền sáng */
    .main { background-color: #f0f2f6; }
    
    /* Ép font và định dạng cho khung Kết quả & Tính toán */
    .calculation-box {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.4;
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #d1d9e6;
        white-space: pre;
        overflow-x: auto;
    }
    .bold-blue { color: #004aad; font-weight: bold; }
    .bold-orange { color: #e65c00; font-weight: bold; font-style: italic; }
    
    /* Chỉnh màu cho Metric để không bị trắng chữ trên nền trắng */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d9e6;
        padding: 10px;
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] > div { color: #004aad !important; }
    [data-testid="stMetricLabel"] > div { color: #333333 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- TỪ ĐIỂN VẬT LIỆU ---
MATERIALS = {
    "Giấy Ivory 300gsm": {"t": 0.35},
    "Giấy Ivory 400gsm": {"t": 0.45},
    "Giấy Duplex 350gsm": {"t": 0.45},
    "Giấy Duplex 400gsm": {"t": 0.50},
    "Sóng E_3 lớp": {"t": 2.0},
    "Sóng B_3 lớp": {"t": 3.0},
    "Sóng C_3 lớp": {"t": 4.0},
    "Sóng B/E_5 lớp": {"t": 4.5},
    "Sóng B/C_5 lớp": {"t": 7.0},
    "Tự nhập (mm)": {"t": 0.0}
}

st.title("📦 QuickDimension - Pro Web Version")
st.caption("Developed by Thanh Dat | Shyft Global - Packaging Team")

# ==========================================
# SIDEBAR NHẬP LIỆU
# ==========================================
with st.sidebar:
    st.header("⚙️ THÔNG SỐ ĐẦU VÀO")
    
    with st.expander("1. HỘP MÀU (COLOR BOX)", expanded=True):
        cb_type = st.radio("Kiểu nhập:", ["Phủ bì (OD)", "Dieline"], horizontal=True)
        cb_mat = st.selectbox("Vật liệu CB:", list(MATERIALS.keys()), index=4)
        t_cb = st.number_input("Độ dày CB (mm):", value=MATERIALS[cb_mat]["t"] if cb_mat != "Tự nhập (mm)" else 1.5)
        
        st.write("**Hệ số bù Tolerance (mm):**")
        c1, c2 = st.columns(2)
        cb_id_l = c1.number_input("+ID L", value=0.0)
        cb_id_w = c2.number_input("+ID W", value=0.0)
        cb_id_h = c1.number_input("+ID H", value=0.0)
        cb_od_l = c2.number_input("+OD L", value=0.0)
        cb_od_w = c1.number_input("+OD W", value=0.0)
        cb_od_h = c2.number_input("+OD H", value=0.0)
        
        st.write("**Kích thước gốc:**")
        l1, w1, h1 = st.columns(3)
        input_l = l1.number_input("L1", value=247.0)
        input_w = w1.number_input("W1", value=90.0)
        input_h = h1.number_input("H1", value=257.0)

    with st.expander("2. INNER CARTON", expanded=True):
        in_mat = st.selectbox("Vật liệu Inner:", list(MATERIALS.keys()), index=5)
        t_in = st.number_input("Độ dày In (mm):", value=MATERIALS[in_mat]["t"] if in_mat != "Tự nhập (mm)" else 3.0)
        
        st.write("**Số lượng xếp (X,Y,Z):**")
        inx, iny, inz = st.columns(3)
        ix = int(inx.number_input("Trục X", value=1))
        iy = int(iny.number_input("Trục Y", value=3))
        iz = int(inz.number_input("Trục Z", value=1))
        
        st.write("**Hệ số bù Tolerance:**")
        i1, i2 = st.columns(2)
        in_id_l = i1.number_input("In ID L", value=3.0)
        in_id_w = i2.number_input("In ID W", value=3.0)
        in_id_h = i1.number_input("In ID H", value=0.0)
        in_od_l = i2.number_input("In OD L", value=1.0)
        in_od_w = i1.number_input("In OD W", value=1.0)
        in_od_h = i2.number_input("In OD H", value=1.0)

    with st.expander("3. MASTER CARTON", expanded=True):
        ma_mat = st.selectbox("Vật liệu Master:", list(MATERIALS.keys()), index=8)
        t_ma = st.number_input("Độ dày Ma (mm):", value=MATERIALS[ma_mat]["t"] if ma_mat != "Tự nhập (mm)" else 7.0)
        
        st.write("**Số lượng xếp:**")
        m_x, m_y, m_z = st.columns(3)
        mx = int(m_x.number_input("Ma X", value=2))
        my = int(m_y.number_input("Ma Y", value=1))
        mz = int(m_z.number_input("Ma Z", value=2))
        
        st.write("**Hệ số bù Tolerance:**")
        m1, m2 = st.columns(2)
        ma_id_l = m1.number_input("Ma ID L", value=3.0)
        ma_id_w = m2.number_input("Ma ID W", value=3.0)
        ma_id_h = m1.number_input("Ma ID H", value=0.0)
        ma_od_l = m2.number_input("Ma OD L", value=1.0)
        ma_od_w = m1.number_input("Ma OD W", value=1.0)
        ma_od_h = m2.number_input("Ma OD H", value=1.0)

# ==========================================
# LOGIC TÍNH TOÁN (COPY TỪ CODE GỐC)
# ==========================================
raw_cb_l = input_l + cb_id_l
raw_cb_w = input_w + cb_id_w
raw_cb_h = input_h + cb_id_h
if cb_type != "Phủ bì (OD)":
    raw_cb_l += t_cb + cb_od_l
    raw_cb_w += t_cb + cb_od_w
    raw_cb_h += t_cb + (cb_od_h * 2)
cb_L, cb_W, cb_H = max(raw_cb_l, raw_cb_w), min(raw_cb_l, raw_cb_w), raw_cb_h

id_in_l = (ix * cb_L) + in_id_l
id_in_w = (iy * cb_W) + in_id_w
id_in_h = (iz * cb_H) + in_id_h
raw_die_in_l, raw_die_in_w, raw_die_in_h = id_in_l + t_in, id_in_w + t_in, id_in_h + (t_in * 2)
raw_od_in_l = id_in_l + (2 * t_in) + in_od_l
raw_od_in_w = id_in_w + (2 * t_in) + in_od_w
raw_od_in_h = id_in_h + (4 * t_in) + in_od_h

is_in_rotated = raw_od_in_l < raw_od_in_w
if not is_in_rotated:
    in_OD_L, in_OD_W, in_OD_H = raw_od_in_l, raw_od_in_w, raw_od_in_h
    in_DIE_L, in_DIE_W, in_DIE_H = raw_die_in_l, raw_die_in_w, raw_die_in_h
else:
    in_OD_L, in_OD_W, in_OD_H = raw_od_in_w, raw_od_in_l, raw_od_in_h
    in_DIE_L, in_DIE_W, in_DIE_H = raw_die_in_w, raw_die_in_l, raw_die_in_h

id_ma_l = (mx * in_OD_L) + ma_id_l
id_ma_w = (my * in_OD_W) + ma_id_w
id_ma_h = (mz * in_OD_H) + ma_id_h
raw_die_ma_l, raw_die_ma_w, raw_die_ma_h = id_ma_l + t_ma, id_ma_w + t_ma, id_ma_h + (t_ma * 2)
raw_od_ma_l = id_ma_l + (2 * t_ma) + ma_od_l
raw_od_ma_w = id_ma_w + (2 * t_ma) + ma_od_w
raw_od_ma_h = id_ma_h + (4 * t_ma) + ma_od_h

is_ma_rotated = raw_od_ma_l < raw_od_ma_w
if not is_ma_rotated:
    ma_OD_L, ma_OD_W, ma_OD_H = raw_od_ma_l, raw_od_ma_w, raw_od_ma_h
    ma_DIE_L, ma_DIE_W, ma_DIE_H = raw_die_ma_l, raw_die_ma_w, raw_die_ma_h
else:
    ma_OD_L, ma_OD_W, ma_OD_H = raw_od_ma_w, raw_od_ma_l, raw_od_ma_h
    ma_DIE_L, ma_DIE_W, ma_DIE_H = raw_die_ma_w, raw_die_ma_l, raw_die_ma_h

# ==========================================
# HIỂN THỊ KẾT QUẢ
# ==========================================
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("🏁 DIELINE KẾT QUẢ")
    m1, m2 = st.columns(2)
    m1.metric("DIELINE INNER", f"{in_DIE_L:.1f} x {in_DIE_W:.1f} x {in_DIE_H:.1f}")
    m2.metric("DIELINE MASTER", f"{ma_DIE_L:.1f} x {ma_DIE_W:.1f} x {ma_DIE_H:.1f}")

    # --- MÔ PHỎNG 3D FIX LỖI ---
    st.subheader("📐 MÔ PHỎNG 3D")
    toggles = st.columns(3)
    s_ma = toggles[0].checkbox("Master", value=True)
    s_in = toggles[1].checkbox("Inner", value=True)
    s_cb = toggles[2].checkbox("Hộp màu", value=True)

    fig = go.Figure()

    def add_wireframe_box(x0, y0, z0, dx, dy, dz, color, name, dash=None):
        # 12 cạnh của khối hộp để không bị nối dây lòng thòng
        lines = [
            ([x0, x0+dx], [y0, y0], [z0, z0]), ([x0+dx, x0+dx], [y0, y0+dy], [z0, z0]),
            ([x0+dx, x0], [y0+dy, y0+dy], [z0, z0]), ([x0, x0], [y0+dy, y0], [z0, z0]),
            ([x0, x0+dx], [y0, y0], [z0+dz, z0+dz]), ([x0+dx, x0+dx], [y0, y0+dy], [z0+dz, z0+dz]),
            ([x0+dx, x0], [y0+dy, y0+dy], [z0+dz, z0+dz]), ([x0, x0], [y0+dy, y0], [z0+dz, z0+dz]),
            ([x0, x0], [y0, y0], [z0, z0+dz]), ([x0+dx, x0+dx], [y0, y0], [z0, z0+dz]),
            ([x0+dx, x0+dx], [y0+dy, y0+dy], [z0, z0+dz]), ([x0, x0], [y0+dy, y0+dy], [z0, z0+dz])
        ]
        for lx, ly, lz in lines:
            fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz, mode='lines', 
                                       line=dict(color=color, width=3, dash=dash), showlegend=False))

    if s_ma:
        add_wireframe_box(0, 0, 0, raw_od_ma_l, raw_od_ma_w, raw_od_ma_h, "#8a949e", "Master")

    # Căn giữa Inner vào Master
    off_in_x = (raw_od_ma_l - mx * in_OD_L) / 2
    off_in_y = (raw_od_ma_w - my * in_OD_W) / 2
    off_in_z = (raw_od_ma_h - mz * in_OD_H) / 2

    if (s_in or s_cb) and (ix*iy*iz*mx*my*mz < 400):
        for xi in range(mx):
            for yi in range(my):
                for zi in range(mz):
                    cur_in_x = off_in_x + xi * in_OD_L
                    cur_in_y = off_in_y + yi * in_OD_W
                    cur_in_z = off_in_z + zi * in_OD_H
                    if s_in:
                        add_wireframe_box(cur_in_x, cur_in_y, cur_in_z, in_OD_L, in_OD_W, in_OD_H, "#0066cc", "Inner")
                    
                    if s_cb:
                        # Căn giữa CB vào Inner
                        # Chú ý: CB_L và CB_W đã được swap trong logic tính toán
                        if is_in_rotated: l_cb, w_cb = cb_W, cb_L
                        else: l_cb, w_cb = cb_L, cb_W
                        
                        off_cb_x = (in_OD_L - (ix if not is_in_rotated else iy) * l_cb) / 2
                        off_cb_y = (in_OD_W - (iy if not is_in_rotated else ix) * w_cb) / 2
                        off_cb_z = (in_OD_H - iz * cb_H) / 2
                        
                        for xc in range(ix if not is_in_rotated else iy):
                            for yc in range(iy if not is_in_rotated else ix):
                                for zc in range(iz):
                                    add_wireframe_box(cur_in_x + off_cb_x + xc*l_cb, 
                                                      cur_in_y + off_cb_y + yc*w_cb, 
                                                      cur_in_z + off_cb_z + zc*cb_H, 
                                                      l_cb, w_cb, cb_H, "#ff1493", "CB", dash="dash")

    fig.update_layout(scene=dict(aspectmode='data'), height=600, margin=dict(l=0,r=0,b=0,t=0))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📜 CHI TIẾT TÍNH TOÁN")
    
    # Xây dựng nội dung Text y hệt Tkinter nhưng dùng HTML/CSS để tô màu
    steps = f"""<div class="calculation-box">
<span class="bold-blue">[1. HỘP MÀU]</span>
  ↳ Gốc nhập: L {input_l} | W {input_w} | H {input_h}
  ↳ Hệ số bù: ID (+{cb_id_l}, +{cb_id_w}, +{cb_id_h}) | OD (+{cb_od_l}, +{cb_od_w}, +{cb_od_h})
<span class="bold-blue">  L1 = {cb_L:.1f} | W1 = {cb_W:.1f} | H1 = {cb_H:.1f} mm</span>

-------------------------------------------------------
<span class="bold-blue">[2. INNER CARTON] - Vật liệu dày: {t_in}mm</span>

<span class="bold-orange">▶ TÍNH TOÁN LỌT LÒNG (INSIDE):</span>
  ↳ <b>ID_L2</b>   = ({ix}xL1) + {in_id_l:<7} = {id_in_l:.1f} mm
  ↳ <b>ID_W2</b>   = ({iy}xW1) + {in_id_w:<7} = {id_in_w:.1f} mm
  ↳ <b>ID_H2</b>   = ({iz}xH1) + {in_id_h:<7} = {id_in_h:.1f} mm

<span class="bold-orange">▶ TÍNH TOÁN TRẢI PHẲNG (DIELINE):</span>
  ↳ <b>DIE_L2</b>  = ID_L2 + {t_in:<7} = {raw_die_in_l:.1f} mm
  ↳ <b>DIE_W2</b>  = ID_W2 + {t_in:<7} = {raw_die_in_w:.1f} mm
  ↳ <b>DIE_H2</b>  = ID_H2 + ({t_in}*2)     = {raw_die_in_h:.1f} mm

<span class="bold-orange">▶ TÍNH TOÁN PHỦ BÌ (OUTSIDE):</span>
  ↳ <b>OD_L2</b>   = ID_L2 + (2*{t_in}) + {in_od_l:<2} = {raw_od_in_l:.1f} mm
  ↳ <b>OD_W2</b>   = ID_W2 + (2*{t_in}) + {in_od_w:<2} = {raw_od_in_w:.1f} mm
  ↳ <b>OD_H2</b>   = ID_H2 + (4*{t_in}) + {in_od_h:<2} = {raw_od_in_h:.1f} mm
<span class="bold-blue"> => CHỐT INNER: L2={in_OD_L:.1f} | W2={in_OD_W:.1f} | H2={in_OD_H:.1f}</span>

-------------------------------------------------------
<span class="bold-blue">[3. MASTER CARTON] - Vật liệu dày: {t_ma}mm</span>

<span class="bold-orange">▶ TÍNH TOÁN LỌT LÒNG (INSIDE):</span>
  ↳ <b>ID_L3</b>   = ({mx}xL2) + {ma_id_l:<7} = {id_ma_l:.1f} mm
  ↳ <b>ID_W3</b>   = ({my}xW2) + {ma_id_w:<7} = {id_ma_w:.1f} mm
  ↳ <b>ID_H3</b>   = ({mz}xH2) + {ma_id_h:<7} = {id_ma_h:.1f} mm

<span class="bold-orange">▶ TÍNH TOÁN TRẢI PHẲNG (DIELINE):</span>
  ↳ <b>DIE_L3</b>  = ID_L3 + {t_ma:<7} = {raw_die_ma_l:.1f} mm
  ↳ <b>DIE_W3</b>  = ID_W3 + {t_ma:<7} = {raw_die_ma_w:.1f} mm
  ↳ <b>DIE_H3</b>  = ID_H3 + ({t_ma}*2)     = {raw_die_ma_h:.1f} mm

<span class="bold-orange">▶ TÍNH TOÁN PHỦ BÌ (OUTSIDE):</span>
  ↳ <b>OD_L3</b>   = ID_L3 + (2*{t_ma}) + {ma_od_l:<2} = {raw_od_ma_l:.1f} mm
  ↳ <b>OD_W3</b>   = ID_W3 + (2*{t_ma}) + {ma_od_w:<2} = {raw_od_ma_w:.1f} mm
  ↳ <b>OD_H3</b>   = ID_H3 + (4*{t_ma}) + {ma_od_h:<2} = {raw_od_ma_h:.1f} mm
<span class="bold-blue"> => CHỐT MASTER: L3={ma_OD_L:.1f} | W3={ma_OD_W:.1f} | H3={ma_OD_H:.1f}</span>
</div>"""
    st.markdown(steps, unsafe_allow_html=True)

# ==========================================
# XUẤT FILE JSX (Giữ nguyên gốc)
# ==========================================
st.markdown("---")
if st.button("📥 Tải Script JSX cho Adobe Illustrator"):
    # Chỗ này anh có thể dán đoạn JSX khổng lồ ở các phiên bản trước vào nhé.
    # Tôi tạm để logic cơ bản để tránh làm loãng code.
    st.info("Anh copy đoạn JSX cũ dán vào biến jsx_script bên dưới là xong.")
