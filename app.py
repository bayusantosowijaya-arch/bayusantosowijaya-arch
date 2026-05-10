import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Simulasi KPR Free PPN", layout="wide")

st.title("🏠 Simulasi KPR Free PPN 2026")
st.markdown("**Free PPN 100% (< 2M) | Free PPN Rp 220 Juta (≥ 2M)**")

col1, col2 = st.columns(2)
with col1:
    harga = st.number_input("Harga Rumah (Rp)", value=1946801250, step=1000000)
    dp_persen = st.slider("DP (%)", 5, 30, 10)

with col2:
    bunga = st.number_input("Suku Bunga (%)", value=3.70, step=0.05)
    tenor = st.selectbox("Tenor (Tahun)", [5,8,10,15,20,25], index=4)

if harga < 2000000000:
    ppn = harga * 0.11
    ket = "Free PPN 100%"
else:
    ppn = 220000000
    ket = "Free PPN Rp 220 Juta"

harga_jual = harga - ppn
dp = harga_jual * (dp_persen / 100)
plafon = harga_jual - dp

def hitung_angsuran(pokok, rate, tahun):
    r = rate / 100 / 12
    n = tahun * 12
    if r == 0:
        return pokok / n
    return pokok * (r * (1 + r)**n) / ((1 + r)**n - 1)

angsuran = hitung_angsuran(plafon, bunga, tenor)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.metric("Harga Rumah", f"Rp {harga:,.0f}")
    st.metric("PPN Ditanggung", f"Rp {ppn:,.0f}", ket)
    st.metric("Harga Jual", f"Rp {harga_jual:,.0f}")
    st.metric("Down Payment", f"Rp {dp:,.0f} ({dp_persen}%)")

with c2:
    st.metric("Plafon KPR", f"Rp {plafon:,.0f}")
    st.metric("Angsuran Bulanan", f"Rp {angsuran:,.0f}", f"{tenor} Tahun")

st.subheader("Simulasi 12 Bulan Pertama")
data = []
sisa = plafon
r = bunga / 100 / 12
for i in range(1,13):
    bunga_bln = sisa * r
    pokok_bln = angsuran - bunga_bln
    sisa -= pokok_bln
    data.append([i, round(angsuran), round(pokok_bln), round(bunga_bln), round(sisa)])

df = pd.DataFrame(data, columns=["Bulan","Angsuran","Pokok","Bunga","Sisa Pokok"])
st.dataframe(df.style.format("{:,.0f}"), use_container_width=True)

if st.button("📥 Download Excel", type="primary"):
    output = pd.ExcelWriter("simulasi_kpr.xlsx", engine='openpyxl')
    pd.DataFrame({
        "Keterangan": ["Harga Rumah", "PPN", "Harga Jual", "DP", "Plafon", "Bunga", "Tenor", "Angsuran"],
        "Nilai": [harga, ppn, harga_jual, dp, plafon, f"{bunga}%", f"{tenor} Tahun", angsuran]
    }).to_excel(output, sheet_name="Ringkasan", index=False)
    df.to_excel(output, sheet_name="12 Bulan", index=False)
    output.close()
    
    with open("simulasi_kpr.xlsx", "rb") as f:
        st.download_button("💾 Simpan File Excel", f.read(), 
                          f"Simulasi_KPR_{datetime.now().strftime('%Y%m%d')}.xlsx",
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.caption("Simulasi Free PPN 2026")
