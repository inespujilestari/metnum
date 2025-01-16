import streamlit as st
import numpy as np
import sympy as sp

# Pengaturan tema dan gaya
st.set_page_config(page_title="Metode Secant", page_icon="🧮", layout="wide")
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        color: #4CAF50;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Judul aplikasi
st.markdown('<h1 class="title">Metode Secant</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Temukan akar fungsi dengan cepat</h3>', unsafe_allow_html=True)

# Penjelasan aplikasi
with st.expander("📘 Apa itu Metode Secant?"):
    st.markdown(
        """
        Metode Secant adalah algoritma numerik untuk mencari akar dari sebuah fungsi kontinu. 
        Teknik ini menggunakan pendekatan berbasis dua titik awal dan iterasi untuk menemukan akar.
        
        **Keunggulan**:
        - Tidak memerlukan turunan fungsi seperti metode Newton-Raphson.
        - Cepat dan sederhana.

        """, unsafe_allow_html=True
    )

# Input fungsi oleh pengguna
st.markdown("---")
st.subheader("🔢 Masukkan Fungsi")
func_str = st.text_input("Fungsi (contoh: x**3 - x - 2)", "x**3 - x - 2")
x = sp.Symbol('x') 
try:
    func = sp.sympify(func_str)
except:
    st.error("❌ Fungsi tidak valid. Periksa input Anda.")
    st.stop()

# Input parameter metode Secant
st.markdown("---")
st.subheader("⚙️ Parameter Secant")
col1, col2, col3 = st.columns(3)
with col1:
    x0 = st.number_input("Tebakan awal (x0):", value=1.0)
with col2:
    x1 = st.number_input("Tebakan awal kedua (x1):", value=2.0)
with col3:
    tolerance = st.number_input("Toleransi (epsilon):", value=1e-5, format="%.5e")
max_iter = st.slider("🔄 Maksimal iterasi:", min_value=1, max_value=100, value=50)

# Definisi fungsi evaluasi
f = sp.lambdify(x, func) 

# Tombol untuk menjalankan metode
if st.button("🔍 Cari Akar"):
    # Inisialisasi variabel
    iter_count = 0
    root = None
    x_vals = [x0, x1]
    error_vals = []

    try:
        while iter_count < max_iter:
            f_x0 = f(x_vals[-2])
            f_x1 = f(x_vals[-1])

            # Hindari pembagian dengan nol
            if abs(f_x1 - f_x0) < 1e-12:
                st.error("❌ Metode gagal karena pembagian dengan nol.")
                st.stop()

            # Hitung nilai baru
            x_new = x_vals[-1] - f_x1 * (x_vals[-1] - x_vals[-2]) / (f_x1 - f_x0)
            error = abs(x_new - x_vals[-1])
            error_vals.append(error)

            # Perbarui nilai
            x_vals.append(x_new)
            iter_count += 1

            # Periksa toleransi
            if error < tolerance:
                root = x_new
                break

        # Tampilkan hasil
        if root is not None:
            st.success(f"✅ Akar ditemukan: x = {root:.6f} setelah {iter_count} iterasi")
        else:
            st.warning("⚠️ Akar tidak ditemukan dalam batas iterasi yang diberikan.")

        # Tampilkan data iterasi
        result_table = {
            "Iterasi": list(range(1, len(x_vals))),
            "x_n": x_vals[1:],
            "Error": error_vals,
        }
        st.markdown("### 📊 Hasil Iterasi")
        st.dataframe(result_table)

        # Visualisasi konvergensi
        st.markdown("### 📈 Konvergensi")
        st.line_chart(error_vals)

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {str(e)}")

# Catatan
with st.expander("📌 Catatan Penting"):
    st.markdown(
        """
        - Pastikan fungsi kontinu pada interval tertentu.
        - Jika metode gagal, coba ubah tebakan awal atau parameter lainnya.
        - Metode ini cocok untuk fungsi non-linear sederhana.
        """
    )
