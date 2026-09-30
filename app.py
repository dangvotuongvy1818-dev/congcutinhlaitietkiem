import streamlit as st

# Cấu hình trang ứng dụng
st.set_page_config(
    page_title="App Tính Lãi Gửi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("💰 Ứng Dụng Tính Lãi Gửi Tiết Kiệm")
st.write("Tính toán tiền lãi đơn và lãi kép dựa trên hình thức lãnh lãi bạn chọn.")

# Giao diện nhập liệu từ người dùng
st.header("1. Nhập thông tin gửi tiết kiệm")

col1, col2 = st.columns(2)

with col1:
    so_tien_goc = st.number_input(
        "Số tiền gửi (VNĐ):", 
        min_value=1_000_000, 
        value=100_000_000, 
        step=1_000_000, 
        format="%d"
    )
    
    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (tháng):", 
        min_value=1, 
        value=12, 
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất năm (%):", 
        min_value=0.0, 
        max_value=20.0, 
        value=6.0, 
        step=0.1
    )
    
    hinh_thuc_lanh_lai = st.selectbox(
        "Hình thức lãnh lãi:",
        ["Lãnh lãi cuối kỳ", "Lãnh lãi theo tháng", "Lãnh lãi theo quý"]
    )

st.header("2. Kết quả tính toán")

# Khởi tạo các biến kết quả
tien_lai_dinh_ky = 0.0
tong_tien_lai_don = 0.0
tong_tien_lai_kep = 0.0

# ----------------- LOGIC TÍNH TOÁN -----------------

# 1. Tính toán LÃI ĐƠN
if hinh_thuc_lanh_lai == "Lãnh lãi cuối kỳ":
    tong_tien_lai_don = so_tien_goc * (lai_suat_nam / 100) * (ky_han_thang / 12)
    tien_lai_dinh_ky = tong_tien_lai_don  # Chỉ nhận 1 lần duy nhất lúc cuối kỳ

elif hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":
    # Lãi đơn nhận hàng tháng
    tien_lai_dinh_ky = so_tien_goc * ((lai_suat_nam / 100) / 12)
    tong_tien_lai_don = tien_lai_dinh_ky * ky_han_thang

elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":
    # Lãi đơn nhận hàng quý (mỗi 3 tháng)
    so_quy = ky_han_thang / 3
    tien_lai_dinh_ky = so_tien_goc * ((lai_suat_nam / 100) / 4)
    tong_tien_lai_don = tien_lai_dinh_ky * so_quy


# 2. Tính toán LÃI KÉP (Lãi nhập gốc)
if hinh_thuc_lanh_lai == "Lãnh lãi cuối kỳ":
    # Cuối kỳ mới nhập gốc (bản chất tương đương lãi đơn trong 1 kỳ hạn)
    tong_tien_lai_kep = tong_tien_lai_don

elif hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":
    # Lãi nhập gốc mỗi tháng
    tong_goc_va_lai_kep = so_tien_goc * ((1 + (lai_suat_nam / 100) / 12) ** ky_han_thang)
    tong_tien_lai_kep = tong_goc_va_lai_kep - so_tien_goc

elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":
    # Lãi nhập gốc mỗi quý (mỗi 3 tháng)
    so_quy = ky_han_thang / 3
    tong_goc_va_lai_kep = so_tien_goc * ((1 + (lai_suat_nam / 100) / 4) ** so_quy)
    tong_tien_lai_kep = tong_goc_va_lai_kep - so_tien_goc

# ----------------- HIỂN THỊ KẾT QUẢ -----------------

tab1, tab2 = st.tabs(["📊 Phương án Lãi Đơn", "📈 Phương án Lãi Kép"])

with tab1:
    st.subheader("Kết quả theo Lãi Đơn")
    st.metric(label="Tiền lãi định kỳ nhận được:", value=f"{tien_lai_dinh_ky:,.0f} VNĐ")
    st.metric(label="Tổng số tiền lãi:", value=f"{tong_tien_lai_don:,.0f} VNĐ")
    st.metric(label="Tổng số tiền gốc + lãi:", value=f"{so_tien_goc + tong_tien_lai_don:,.0f} VNĐ")
    
    if hinh_thuc_lanh_lai != "Lãnh lãi cuối kỳ":
        chu_ky = "tháng" if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng" else "quý"
        st.caption(f"(*) Bạn sẽ nhận đều đặn {tien_lai_dinh_ky:,.0f} VNĐ mỗi {chu_ky} cho đến hết kỳ hạn.")

with tab2:
    st.subheader("Kết quả theo Lãi Kép (Lãi nhập gốc)")
    st.metric(label="Tổng số tiền lãi kép:", value=f"{tong_tien_lai_kep:,.0f} VNĐ")
    st.metric(label="Tổng số tiền gốc + lãi kép:", value=f"{so_tien_goc + tong_tien_lai_kep:,.0f} VNĐ")
    st.caption("(*) Lãi kép áp dụng khi tiền lãi định kỳ của bạn được tự động cộng dồn vào tiền gốc để tính lãi cho kỳ tiếp theo.")
