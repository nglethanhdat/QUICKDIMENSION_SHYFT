import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==========================================
# CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(page_title="QuickDimension - Pro Web Version", page_icon="📦", layout="wide")

# FIX LỖI TÀNG HÌNH CHỮ: Ép màu nền sáng và màu chữ tối cho mọi thành phần bên trong
st.markdown("""
    <style>
    /* Chỉnh màu cho khung Metric */
    [data-testid="stMetric"] { background-color: #f8f9fa !important; padding: 15px; border-radius: 8px; border-left: 5px solid #004aad; }
    [data-testid="stMetricLabel"] * { color: #333333 !important; font-weight: bold; font-size: 16px !important;}
    [data-testid="stMetricValue"] * { color: #004aad !important; font-size: 24px !important;}
    
    /* Chỉnh màu cho khung Text Step */
    .step-text { font-family: 'Consolas', monospace; font-size: 14px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #ddd; white-space: pre-wrap; color: #111111 !important; }
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

st.title("📦 QuickDimension - Pro Web Version")
st.caption("Developed by Thanh Dat | Shyft Global - Packaging Team | Powered by AI Sarcasm")

# ==========================================
# GIAO DIỆN NHẬP LIỆU (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("⚙️ THÔNG SỐ ĐẦU VÀO")
    
    # --- 1. HỘP MÀU ---
    with st.expander("1. HỘP MÀU (COLOR BOX)", expanded=True):
        cb_input_type = st.radio("Kiểu nhập:", ["Phủ bì (OD)", "Dieline"], index=0, horizontal=True)
        cb_mat = st.selectbox("Vật liệu:", list(MATERIALS.keys()), index=4)
        
        cb_custom_thick = 1.5
        if cb_mat == "Tự nhập (mm)":
            cb_custom_thick = st.number_input("Độ dày tự nhập (mm):", min_value=0.0, value=1.5, step=0.1)
            t_cb = cb_custom_thick
        else:
            t_cb = MATERIALS[cb_mat]["t"]

        st.markdown("**+ID (L,W,H) [Bù lọt lòng]:**")
        c_id_l, c_id_w, c_id_h = st.columns(3)
        cb_id_l = c_id_l.number_input("ID L1", value=0.0, step=1.0)
        cb_id_w = c_id_w.number_input("ID W1", value=0.0, step=1.0)
        cb_id_h = c_id_h.number_input("ID H1", value=0.0, step=1.0)

        st.markdown("**+OD (L,W,H) [Bù phủ bì]:**")
        c_od_l, c_od_w, c_od_h = st.columns(3)
        cb_od_l = c_od_l.number_input("OD L1", value=0.0, step=1.0)
        cb_od_w = c_od_w.number_input("OD W1", value=0.0, step=1.0)
        cb_od_h = c_od_h.number_input("OD H1", value=0.0, step=1.0)

        st.markdown("**Kích thước gốc:**")
        c_l, c_w, c_h = st.columns(3)
        input_l = c_l.number_input("Dài L1", value=247.0, step=1.0)
        input_w = c_w.number_input("Rộng W1", value=90.0, step=1.0)
        input_h = c_h.number_input("Cao H1", value=257.0, step=1.0)

    # --- 2. INNER CARTON ---
    with st.expander("2. INNER CARTON (XẾP HỘP MÀU)", expanded=True):
        in_mat = st.selectbox("Vật liệu Inner:", list(MATERIALS.keys()), index=5)
        in_custom_thick = 3.0
        if in_mat == "Tự nhập (mm)":
            in_custom_thick = st.number_input("Độ dày Inner tự nhập (mm):", min_value=0.0, value=3.0, step=0.1)
            t_in = in_custom_thick
        else:
            t_in = MATERIALS[in_mat]["t"]

        c_inx, c_iny, c_inz = st.columns(3)
        ix = int(c_inx.number_input("Trục X (L1)", value=1, min_value=0))
        iy = int(c_iny.number_input("Trục Y (W1)", value=3, min_value=0))
        iz = int(c_inz.number_input("Trục Z (H1)", value=1, min_value=0))

        st.markdown("**+ID (L,W,H) Inner:**")
        i_id_l, i_id_w, i_id_h = st.columns(3)
        in_id_l = i_id_l.number_input("In ID L", value=3.0, step=1.0)
        in_id_w = i_id_w.number_input("In ID W", value=3.0, step=1.0)
        in_id_h = i_id_h.number_input("In ID H", value=0.0, step=1.0)

        st.markdown("**+OD (L,W,H) Inner:**")
        i_od_l, i_od_w, i_od_h = st.columns(3)
        in_od_l = i_od_l.number_input("In OD L", value=1.0, step=1.0)
        in_od_w = i_od_w.number_input("In OD W", value=1.0, step=1.0)
        in_od_h = i_od_h.number_input("In OD H", value=1.0, step=1.0)

    # --- 3. MASTER CARTON ---
    with st.expander("3. MASTER CARTON (XẾP INNER)", expanded=True):
        ma_mat = st.selectbox("Vật liệu Master:", list(MATERIALS.keys()), index=8)
        ma_custom_thick = 7.0
        if ma_mat == "Tự nhập (mm)":
            ma_custom_thick = st.number_input("Độ dày Master tự nhập (mm):", min_value=0.0, value=7.0, step=0.1)
            t_ma = ma_custom_thick
        else:
            t_ma = MATERIALS[ma_mat]["t"]

        c_max, c_may, c_maz = st.columns(3)
        mx = int(c_max.number_input("Trục X (L2)", value=2, min_value=0))
        my = int(c_may.number_input("Trục Y (W2)", value=1, min_value=0))
        mz = int(c_maz.number_input("Trục Z (H2)", value=2, min_value=0))

        st.markdown("**+ID (L,W,H) Master:**")
        m_id_l, m_id_w, m_id_h = st.columns(3)
        ma_id_l = m_id_l.number_input("Ma ID L", value=3.0, step=1.0)
        ma_id_w = m_id_w.number_input("Ma ID W", value=3.0, step=1.0)
        ma_id_h = m_id_h.number_input("Ma ID H", value=0.0, step=1.0)

        st.markdown("**+OD (L,W,H) Master:**")
        m_od_l, m_od_w, m_od_h = st.columns(3)
        ma_od_l = m_od_l.number_input("Ma OD L", value=1.0, step=1.0)
        ma_od_w = m_od_w.number_input("Ma OD W", value=1.0, step=1.0)
        ma_od_h = m_od_h.number_input("Ma OD H", value=1.0, step=1.0)


# ==========================================
# LOGIC TÍNH TOÁN (Giữ nguyên chuẩn xác)
# ==========================================
raw_cb_l, raw_cb_w, raw_cb_h = input_l + cb_id_l, input_w + cb_id_w, input_h + cb_id_h

if cb_input_type != "Phủ bì (OD)":
    raw_cb_l += t_cb + cb_od_l
    raw_cb_w += t_cb + cb_od_w
    raw_cb_h += t_cb + (cb_od_h * 2) 
    
cb_L, cb_W, cb_H = max(raw_cb_l, raw_cb_w), min(raw_cb_l, raw_cb_w), raw_cb_h

id_in_l = (ix * cb_L) + in_id_l
id_in_w = (iy * cb_W) + in_id_w
id_in_h = (iz * cb_H) + in_id_h

raw_die_in_l = id_in_l + t_in
raw_die_in_w = id_in_w + t_in
raw_die_in_h = id_in_h + (t_in * 2) 

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

raw_die_ma_l = id_ma_l + t_ma
raw_die_ma_w = id_ma_w + t_ma
raw_die_ma_h = id_ma_h + (t_ma * 2) 

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
# KHU VỰC HIỂN THỊ CHÍNH
# ==========================================
col_res, col_steps = st.columns([1.5, 1])

with col_res:
    # --- CẢNH BÁO ---
    if ma_OD_L > 1200 or ma_OD_W > 1000:
        st.error(f"⚠ LƯU Ý: Phủ bì Master ({ma_OD_L:.1f}x{ma_OD_W:.1f}) vượt khổ Pallet (1200x1000)!")
    elif ma_OD_H > ma_OD_L * 1.5:
        st.warning("⚠ LƯU Ý: Thùng quá cao so với mặt đáy, nguy cơ lật khi xếp chồng Pallet!")

    # --- KẾT QUẢ RÚT GỌN ---
    st.subheader("🏁 DIELINE XUẤT XƯỞNG")
    st.metric("DIELINE INNER", f"L2 {in_DIE_L:.1f} x W2 {in_DIE_W:.1f} x H2 {in_DIE_H:.1f} mm")
    st.metric("DIELINE MASTER", f"L3 {ma_DIE_L:.1f} x W3 {ma_DIE_W:.1f} x H3 {ma_DIE_H:.1f} mm")

    # --- FIX MÔ PHỎNG 3D: Tính toán lồng ghép chính xác tuyệt đối ---
    st.subheader("📐 MÔ PHỎNG 3D INTERACTIVE (ĐÃ FIX LỖI LÒI RUỘT)")
    st.write("Dùng chuột để xoay và zoom. Vẽ tâm chuẩn 100% không lệch 1 ly.")
    
    col_toggles = st.columns(3)
    show_ma = col_toggles[0].checkbox("Hiển thị Master", value=True)
    show_in = col_toggles[1].checkbox("Hiển thị Inner", value=True)
    show_cb = col_toggles[2].checkbox("Hiển thị Hộp Màu", value=True)

    fig = go.Figure()

    def add_box_trace(x, y, z, dx, dy, dz, color, name):
        # 8 đỉnh của hình hộp 3D thực thụ
        xx = [x, x+dx, x+dx, x, x, x, x+dx, x+dx, x, x, x+dx, x+dx, x+dx, x+dx, x, x]
        yy = [y, y, y+dy, y+dy, y, y, y, y+dy, y+dy, y, y, y, y+dy, y+dy, y+dy, y+dy]
        zz = [z, z, z, z, z, z+dz, z+dz, z+dz, z+dz, z+dz, z+dz, z, z, z+dz, z+dz, z]
        fig.add_trace(go.Scatter3d(x=xx, y=yy, z=zz, mode='lines', line=dict(color=color, width=3), name=name, showlegend=False))

    total_boxes = (ix*iy*iz) * (mx*my*mz)
    if total_boxes > 500:
        st.warning(f"🛑 Cảnh báo: Vẽ {total_boxes} hộp sẽ làm đơ trình duyệt. Tạm ẩn hộp con, chỉ vẽ Master.")
        show_in = False
        show_cb = False

    # Vẽ Master Carton bọc toàn bộ (Sử dụng Raw_OD làm gốc tuyệt đối)
    if show_ma:
        add_box_trace(0, 0, 0, raw_od_ma_l, raw_od_ma_w, raw_od_ma_h, "#8a949e", "Master Carton")

    # Căn giữa cụm Inner Carton vào bên trong Master Carton
    ma_start_x = (raw_od_ma_l - mx * in_OD_L) / 2
    ma_start_y = (raw_od_ma_w - my * in_OD_W) / 2
    ma_start_z = (raw_od_ma_h - mz * in_OD_H) / 2

    if show_in or show_cb:
        for m_x in range(mx):
            for m_y in range(my):
                for m_z in range(mz):
                    # Tọa độ gốc của từng Inner Carton
                    cur_in_x = ma_start_x + m_x * in_OD_L
                    cur_in_y = ma_start_y + m_y * in_OD_W
                    cur_in_z = ma_start_z + m_z * in_OD_H
                    
                    if show_in:
                        add_box_trace(cur_in_x, cur_in_y, cur_in_z, in_OD_L, in_OD_W, in_OD_H, "#0066cc", "Inner Carton")

                    # Căn giữa cụm Color Box vào bên trong Inner Carton hiện tại
                    if show_cb:
                        in_start_x = (in_OD_L - ix * cb_L) / 2
                        in_start_y = (in_OD_W - iy * cb_W) / 2
                        in_start_z = (in_OD_H - iz * cb_H) / 2

                        for i_x in range(ix):
                            for i_y in range(iy):
                                for i_z in range(iz):
                                    cur_cb_x = cur_in_x + in_start_x + i_x * cb_L
                                    cur_cb_y = cur_in_y + in_start_y + i_y * cb_W
                                    cur_cb_z = cur_in_z + in_start_z + i_z * cb_H
                                    
                                    add_box_trace(cur_cb_x, cur_cb_y, cur_cb_z, cb_L, cb_W, cb_H, "#ff1493", "Color Box")

    fig.update_layout(scene=dict(aspectmode='data', xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), height=500, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig, use_container_width=True)

with col_steps:
    st.subheader("📜 CHI TIẾT BƯỚC TÍNH TOÁN")
    
    steps_str = f"""[1. HỘP MÀU]
   ↳ Gốc nhập: L {input_l} | W {input_w} | H {input_h}
   ↳ Hệ số bù: ID (+{cb_id_l}, +{cb_id_w}, +{cb_id_h}) | OD (+{cb_od_l}, +{cb_od_w}, +{cb_od_h})
   L1 = {cb_L:.1f} | W1 = {cb_W:.1f} | H1 = {cb_H:.1f} mm
-------------------------------------------------------
[2. INNER CARTON] - Vật liệu dày: {t_in}mm

▶ TÍNH TOÁN LỌT LÒNG (INSIDE):
  ↳ ID_L2   = ({ix}xL1) + {in_id_l:<14} = {id_in_l:.1f} mm
  ↳ ID_W2   = ({iy}xW1) + {in_id_w:<14} = {id_in_w:.1f} mm
  ↳ ID_H2   = ({iz}xH1) + {in_id_h:<14} = {id_in_h:.1f} mm

▶ TÍNH TOÁN TRẢI PHẲNG (DIELINE):
  ↳ DIE_L2  = ID_L2 + {t_in:<14} = {raw_die_in_l:.1f} mm
  ↳ DIE_W2  = ID_W2 + {t_in:<14} = {raw_die_in_w:.1f} mm
  ↳ DIE_H2  = ID_H2 + ({t_in}*2)          = {raw_die_in_h:.1f} mm

▶ TÍNH TOÁN PHỦ BÌ (OUTSIDE):
  ↳ OD_L2   = ID_L2 + (2*{t_in}) + {in_od_l:<5} = {raw_od_in_l:.1f} mm
  ↳ OD_W2   = ID_W2 + (2*{t_in}) + {in_od_w:<5} = {raw_od_in_w:.1f} mm
  ↳ OD_H2   = ID_H2 + (4*{t_in}) + {in_od_h:<5} = {raw_od_in_h:.1f} mm
 => CHỐT INNER: L2={in_OD_L:.1f} | W2={in_OD_W:.1f} | H2={in_OD_H:.1f}
-------------------------------------------------------
[3. MASTER CARTON] - Vật liệu dày: {t_ma}mm

▶ TÍNH TOÁN LỌT LÒNG (INSIDE):
  ↳ ID_L3   = ({mx}xL2) + {ma_id_l:<14} = {id_ma_l:.1f} mm
  ↳ ID_W3   = ({my}xW2) + {ma_id_w:<14} = {id_ma_w:.1f} mm
  ↳ ID_H3   = ({mz}xH2) + {ma_id_h:<14} = {id_ma_h:.1f} mm

▶ TÍNH TOÁN TRẢI PHẲNG (DIELINE):
  ↳ DIE_L3  = ID_L3 + {t_ma:<14} = {raw_die_ma_l:.1f} mm
  ↳ DIE_W3  = ID_W3 + {t_ma:<14} = {raw_die_ma_w:.1f} mm
  ↳ DIE_H3  = ID_H3 + ({t_ma}*2)          = {raw_die_ma_h:.1f} mm

▶ TÍNH TOÁN PHỦ BÌ (OUTSIDE):
  ↳ OD_L3   = ID_L3 + (2*{t_ma}) + {ma_od_l:<5} = {raw_od_ma_l:.1f} mm
  ↳ OD_W3   = ID_W3 + (2*{t_ma}) + {ma_od_w:<5} = {raw_od_ma_w:.1f} mm
  ↳ OD_H3   = ID_H3 + (4*{t_ma}) + {ma_od_h:<5} = {raw_od_ma_h:.1f} mm
 => CHỐT MASTER: L3={ma_OD_L:.1f} | W3={ma_OD_W:.1f} | H3={ma_OD_H:.1f}
"""
    st.markdown(f'<div class="step-text">{steps_str}</div>', unsafe_allow_html=True)


# ==========================================
# XUẤT SCRIPT JSX CHO ILLUSTRATOR
# ==========================================
st.markdown("---")
st.subheader("📥 XUẤT PDF DIELINE (QUA ILLUSTRATOR)")

jsx_script = """
        var mm2pt = 2.834645;
        var doc = app.documents.add();
        var dimLayer = doc.layers.add(); dimLayer.name = "Dimensions";
        var dieLayer = doc.layers.add(); dieLayer.name = "Diecut";

        var cutColor = new RGBColor(); cutColor.red = 255; cutColor.green = 0; cutColor.blue = 0;
        var creaseColor = new RGBColor(); creaseColor.red = 0; creaseColor.green = 255; creaseColor.blue = 0;
        var dimColor = new RGBColor(); dimColor.red = 100; dimColor.green = 100; dimColor.blue = 100;

        function drawBox(boxName, L, W, H, CAL, GLUE, startX_mm, startY_mm) {
            var L_pt = L * mm2pt; var W_pt = W * mm2pt; var H_pt = H * mm2pt;
            var CAL_pt = CAL * mm2pt; var GLUE_pt = GLUE * mm2pt;
            var startX = startX_mm * mm2pt; var startY = startY_mm * mm2pt;

            var strokeWt = 1.0;
            var flap = (W_pt / 2) + (CAL_pt / 2);
            var gap = CAL_pt / 2;

            var l_first = L_pt - gap;
            var w_last = W_pt - gap;

            var x0 = startX;
            var x1 = startX + GLUE_pt;
            var x2 = x1 + l_first;
            var x3 = x2 + W_pt;
            var x4 = x3 + L_pt;
            var x5 = x4 + w_last;

            var y0 = startY, y1 = startY + flap, y2 = y1 + H_pt, y3 = y2 + flap;

            function drawLine(xS, yS, xE, yE, color, isDashed) {
                var path = dieLayer.pathItems.add();
                path.setEntirePath([[xS, yS], [xE, yE]]);
                path.filled = false; path.stroked = true;
                path.strokeColor = color; path.strokeWidth = strokeWt;
                if (isDashed) path.strokeDashes = [12, 6];
            }

            function drawSlot(xC, yOut, yIn) {
                drawLine(xC - gap, yOut, xC - gap, yIn, cutColor, false);
                drawLine(xC + gap, yOut, xC + gap, yIn, cutColor, false);
                drawLine(xC - gap, yIn, xC + gap, yIn, cutColor, false);
            }

            function drawDim(xS, yS, xE, yE, textLabel, offset, isVert) {
                var pX1 = xS, pY1 = yS, pX2 = xE, pY2 = yE;
                var tX, tY;
                if (isVert) {
                    pX1 -= offset; pX2 -= offset;
                    tX = pX1 - 40; tY = (yS + yE) / 2;
                } else {
                    pY1 += offset; pY2 += offset;
                    tX = (xS + xE) / 2; tY = pY1 + 15;
                }
                var path = dimLayer.pathItems.add();
                path.setEntirePath([[pX1, pY1], [pX2, pY2]]);
                path.filled = false; path.stroked = true;
                path.strokeColor = dimColor; path.strokeWidth = 0.5;

                var t = 5 * mm2pt;
                var tick1 = dimLayer.pathItems.add(); tick1.setEntirePath([[pX1-t, pY1-t], [pX1+t, pY1+t]]); tick1.stroked = true; tick1.strokeColor = dimColor; tick1.strokeWidth = 0.5;
                var tick2 = dimLayer.pathItems.add(); tick2.setEntirePath([[pX2-t, pY2-t], [pX2+t, pY2+t]]); tick2.stroked = true; tick2.strokeColor = dimColor; tick2.strokeWidth = 0.5;

                var textFrame = dimLayer.textFrames.add();
                textFrame.contents = textLabel; textFrame.position = [tX, tY];
                textFrame.textRange.characterAttributes.size = 24;
                textFrame.textRange.characterAttributes.fillColor = dimColor;
                textFrame.textRange.justification = Justification.CENTER;
            }

            drawLine(x1, y1, x5, y1, creaseColor, true);
            drawLine(x1, y2, x5, y2, creaseColor, true);
            drawLine(x1, y1, x1, y2, creaseColor, true);
            drawLine(x2, y1, x2, y2, creaseColor, true);
            drawLine(x3, y1, x3, y2, creaseColor, true);
            drawLine(x4, y1, x4, y2, creaseColor, true);

            drawLine(x1, y2, x0, y2 - 15 * mm2pt, cutColor, false);
            drawLine(x0, y2 - 15 * mm2pt, x0, y1 + 15 * mm2pt, cutColor, false);
            drawLine(x0, y1 + 15 * mm2pt, x1, y1, cutColor, false);
            drawLine(x1, y3, x1, y2, cutColor, false); 
            drawLine(x1, y1, x1, y0, cutColor, false); 

            drawSlot(x2, y3, y2); drawSlot(x3, y3, y2); drawSlot(x4, y3, y2);
            drawSlot(x2, y0, y1); drawSlot(x3, y0, y1); drawSlot(x4, y0, y1);

            drawLine(x1, y3, x2 - gap, y3, cutColor, false);
            drawLine(x2 + gap, y3, x3 - gap, y3, cutColor, false);
            drawLine(x3 + gap, y3, x4 - gap, y3, cutColor, false);
            drawLine(x4 + gap, y3, x5, y3, cutColor, false);

            drawLine(x1, y0, x2 - gap, y0, cutColor, false);
            drawLine(x2 + gap, y0, x3 - gap, y0, cutColor, false);
            drawLine(x3 + gap, y0, x4 - gap, y0, cutColor, false);
            drawLine(x4 + gap, y0, x5, y0, cutColor, false);

            drawLine(x5, y3, x5, y2, cutColor, false);
            drawLine(x5, y2, x5, y1, cutColor, false);
            drawLine(x5, y1, x5, y0, cutColor, false);

            var offY = 30 * mm2pt;
            var offX = 30 * mm2pt;

            drawDim(x1, y3, x2, y3, (l_first/mm2pt).toFixed(1), offY, false);
            drawDim(x2, y3, x3, y3, W.toFixed(1), offY, false);
            drawDim(x3, y3, x4, y3, L.toFixed(1), offY, false);
            drawDim(x4, y3, x5, y3, (w_last/mm2pt).toFixed(1), offY, false);

            drawDim(x0, y1, x0, y2, H.toFixed(1), offX, true);
            drawDim(x1, y2, x1, y3, (flap/mm2pt).toFixed(1), offX, true);
            drawDim(x0, y3, x1, y3, GLUE.toFixed(1), offY, false);

            var title = dimLayer.textFrames.add();
            title.contents = boxName;
            title.position = [startX, y3 + (80 * mm2pt)];
            title.textRange.characterAttributes.size = 50;
            title.textRange.characterAttributes.fillColor = cutColor;
        }

        var show_in = [SHOW_IN];
        var show_ma = [SHOW_MA];

        var inner_y3 = 0;
        var master_y0 = 0;
        var max_x = 0;

        if (show_in) {
            var in_L = [IN_L]; var in_W = [IN_W]; var in_H = [IN_H]; var in_CAL = [IN_CAL];
            drawBox("INNER CARTON (FEFCO 201)", in_L, in_W, in_H, in_CAL, 35, 0, 0);
            
            inner_y3 = (in_H + in_W + in_CAL) * mm2pt;
            max_x = Math.max(max_x, (35 + in_L*2 + in_W*2) * mm2pt);
            master_y0 = 0; 
        }

        if (show_ma) {
            var ma_L = [MA_L]; var ma_W = [MA_W]; var ma_H = [MA_H]; var ma_CAL = [MA_CAL];
            var startY_mm = 0;
            
            if (show_in) {
                var master_total_height_mm = ma_H + ma_W + ma_CAL;
                startY_mm = 0 - master_total_height_mm - 120; 
            }
            
            drawBox("MASTER CARTON (FEFCO 201)", ma_L, ma_W, ma_H, ma_CAL, 40, 0, startY_mm);
            
            master_y0 = startY_mm * mm2pt;
            max_x = Math.max(max_x, (40 + ma_L*2 + ma_W*2) * mm2pt);
            
            if (!show_in) {
                inner_y3 = (ma_H + ma_W + ma_CAL) * mm2pt; 
            }
        }

        var padding = 80 * mm2pt; 
        var abLeft = -padding;
        var abRight = max_x + padding + (50 * mm2pt); 
        var abTop = inner_y3 + padding + (100 * mm2pt); 
        var abBottom = master_y0 - padding - (50 * mm2pt); 

        doc.artboards[0].artboardRect = [abLeft, abTop, abRight, abBottom];
"""

jsx_script = jsx_script.replace("[SHOW_IN]", "true" if (show_in and (ix*iy*iz > 0)) else "false")
jsx_script = jsx_script.replace("[SHOW_MA]", "true" if (show_ma and (mx*my*mz > 0)) else "false")
jsx_script = jsx_script.replace("[IN_L]", str(in_DIE_L))
jsx_script = jsx_script.replace("[IN_W]", str(in_DIE_W))
jsx_script = jsx_script.replace("[IN_H]", str(in_DIE_H))
jsx_script = jsx_script.replace("[IN_CAL]", str(t_in))
jsx_script = jsx_script.replace("[MA_L]", str(ma_DIE_L))
jsx_script = jsx_script.replace("[MA_W]", str(ma_DIE_W))
jsx_script = jsx_script.replace("[MA_H]", str(ma_DIE_H))
jsx_script = jsx_script.replace("[MA_CAL]", str(t_ma))

st.download_button(
    label="📥 Tải file kịch bản (.jsx) về cho Illustrator",
    data=jsx_script,
    file_name="AutoDieline_Export.jsx",
    mime="text/javascript",
    help="Vì đây là Web nên không có chuyện nó tự mở AI giùm đâu nha. Tải về rồi ném vào AI thủ công."
)
st.caption("👉 *Lưu ý: Tải file trên về, mở Adobe Illustrator -> File -> Scripts -> Other Scripts -> Chọn file vừa tải.*")
