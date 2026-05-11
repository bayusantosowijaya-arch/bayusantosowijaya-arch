import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Simulasi KPR – Ruang Masbay",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --gold:#C9A84C; --gold-lt:#E8C97B; --navy:#0D1B2A; --navy-lt:#152336;
    --cream:#F5F0E8; --slate:#6B7A8D; --green:#2ECC71;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--navy);color:var(--cream);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D1B2A 0%,#152336 100%);border-right:1px solid rgba(201,168,76,0.3);}
[data-testid="stSidebar"] label{color:var(--cream)!important;font-weight:500;font-size:0.85rem;letter-spacing:0.05em;text-transform:uppercase;}
.header-wrap{background:linear-gradient(135deg,#152336 0%,#0D1B2A 60%,#1a2840 100%);border:1px solid rgba(201,168,76,0.35);border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.5rem;position:relative;overflow:hidden;}
.header-wrap::before{content:'';position:absolute;top:-40px;right:-40px;width:200px;height:200px;background:radial-gradient(circle,rgba(201,168,76,0.12) 0%,transparent 70%);border-radius:50%;}
.logo-row{display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;}
.logo-icon{font-size:2.8rem;line-height:1;}
.brand-name{font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;background:linear-gradient(135deg,var(--gold-lt),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;}
.brand-tagline{font-size:0.8rem;color:var(--slate);letter-spacing:0.15em;text-transform:uppercase;margin-top:2px;}
.header-title{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:var(--cream);margin-top:0.75rem;}
.header-sub{font-size:0.85rem;color:var(--slate);margin-top:0.25rem;}
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:1.5rem;}
.metric-card{background:linear-gradient(135deg,#152336,#1a2a40);border:1px solid rgba(201,168,76,0.2);border-radius:12px;padding:1.25rem 1.5rem;position:relative;overflow:hidden;transition:border-color 0.3s;}
.metric-card:hover{border-color:rgba(201,168,76,0.55);}
.metric-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--gold-lt));border-radius:0 0 12px 12px;}
.metric-label{font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--slate);margin-bottom:0.4rem;}
.metric-value{font-family:'Playfair Display',serif;font-size:1.45rem;font-weight:700;color:var(--gold-lt);line-height:1.1;}
.metric-value.big{font-size:1.7rem;color:var(--gold);}
.metric-note{font-size:0.72rem;color:var(--slate);margin-top:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;color:var(--gold-lt);border-left:3px solid var(--gold);padding-left:0.75rem;margin:1.5rem 0 1rem;}
.calc-table{width:100%;border-collapse:collapse;font-size:0.88rem;margin-bottom:1rem;}
.calc-table th{background:rgba(201,168,76,0.15);color:var(--gold-lt);font-weight:600;letter-spacing:0.08em;text-transform:uppercase;font-size:0.75rem;padding:0.65rem 1rem;text-align:left;border-bottom:1px solid rgba(201,168,76,0.3);}
.calc-table td{padding:0.6rem 1rem;border-bottom:1px solid rgba(255,255,255,0.05);color:var(--cream);vertical-align:middle;}
.calc-table tr:last-child td{border-bottom:none;}
.calc-table tr:hover td{background:rgba(201,168,76,0.05);}
.calc-table .highlight td{font-weight:600;color:var(--gold-lt);background:rgba(201,168,76,0.08);}
.calc-table .total-row td{font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--gold);background:rgba(201,168,76,0.12);border-top:1px solid rgba(201,168,76,0.4);}
.tag-free{background:rgba(46,204,113,0.2);color:var(--green);border:1px solid rgba(46,204,113,0.4);border-radius:4px;padding:2px 8px;font-size:0.72rem;font-weight:600;}
.tag-220{background:rgba(201,168,76,0.2);color:var(--gold-lt);border:1px solid rgba(201,168,76,0.4);border-radius:4px;padding:2px 8px;font-size:0.72rem;font-weight:600;}
.info-box{background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.25);border-radius:10px;padding:1rem 1.25rem;font-size:0.83rem;color:var(--cream);line-height:1.6;margin-bottom:1rem;}
.info-box strong{color:var(--gold-lt);}
.angsuran-box{background:linear-gradient(135deg,rgba(201,168,76,0.18),rgba(201,168,76,0.06));border:2px solid rgba(201,168,76,0.5);border-radius:14px;padding:1.5rem 2rem;text-align:center;margin-bottom:1.5rem;}
.angsuran-label{font-size:0.78rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--slate);margin-bottom:0.4rem;}
.angsuran-value{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:900;color:var(--gold);}
.angsuran-sub{font-size:0.8rem;color:var(--slate);margin-top:0.3rem;}
.harga-display{background:rgba(201,168,76,0.12);border:1px solid rgba(201,168,76,0.35);border-radius:8px;padding:0.5rem 0.75rem;font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--gold);text-align:center;margin-top:0.3rem;margin-bottom:0.5rem;letter-spacing:0.02em;}
.footer{text-align:center;padding:1.5rem;font-size:0.75rem;color:var(--slate);border-top:1px solid rgba(201,168,76,0.15);margin-top:2rem;letter-spacing:0.05em;}
.footer span{color:var(--gold-lt);}
.gold-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,0.5),transparent);margin:1.5rem 0;}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def fmt_idr(value):
    """Format ke Rp 3.500.000.000"""
    return "Rp {:,.0f}".format(value).replace(",", ".")

def fmt_idr_short(value):
    """Format singkat: Rp 3,500 M / Rp 350 Jt"""
    if value >= 1_000_000_000:
        b = value / 1_000_000_000
        s = "{:.3f}".format(b) if b < 10 else "{:.2f}".format(b)
        return "Rp " + s.replace(".", ",") + " M"
    elif value >= 1_000_000:
        return "Rp {:.1f} Jt".format(value / 1_000_000)
    return "Rp {:,.0f}".format(value).replace(",", ".")

def fmt_ribuan(value):
    """Format angka pakai titik sebagai ribuan: 3.500.000.000"""
    return "{:,.0f}".format(int(value)).replace(",", ".")

def hitung_ppn(harga):
    """
    Free PPN 2026:
    - Harga < Rp 2.000.000.000  → PPN DTP: 11% dari harga, ditanggung pemerintah penuh
    - Harga >= Rp 2.000.000.000 → Free PPN flat Rp 220.000.000 ditanggung pemerintah
    Mengembalikan (ppn_ditanggung_pemerintah, rate_display, keterangan, is_bawah_2m)
    """
    if harga < 2_000_000_000:
        ppn_dtp = harga * 0.11
        return ppn_dtp, 11.0, "DTP 11% ditanggung pemerintah", True
    else:
        ppn_dtp = 220_000_000.0
        rate    = round(ppn_dtp / harga * 100, 2)
        return ppn_dtp, rate, "Flat Rp 220 Jt ditanggung pemerintah", False

def hitung_angsuran(pokok, bunga_tahunan, tenor_bulan):
    if pokok <= 0 or tenor_bulan <= 0:
        return 0.0
    if bunga_tahunan == 0:
        return pokok / tenor_bulan
    r = bunga_tahunan / 100 / 12
    return pokok * r * (1 + r)**tenor_bulan / ((1 + r)**tenor_bulan - 1)

def buat_amortisasi(pokok, bunga_tahunan, tenor_bulan):
    rows = []
    sisa = pokok
    r = bunga_tahunan / 100 / 12
    angsuran = hitung_angsuran(pokok, bunga_tahunan, tenor_bulan)
    for bln in range(1, tenor_bulan + 1):
        bunga_bln   = sisa * r
        cicil_pokok = angsuran - bunga_bln
        sisa       -= cicil_pokok
        rows.append({
            "Bulan":        bln,
            "Angsuran":     round(angsuran),
            "Bunga":        round(bunga_bln),
            "Pokok":        round(cicil_pokok),
            "Sisa Pokok":   round(max(sisa, 0)),
        })
    return rows


# ─── Sidebar Input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem">
        <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:900;
             background:linear-gradient(135deg,#E8C97B,#C9A84C);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
             🏠 Ruang Masbay</div>
        <div style="font-size:0.7rem;color:#6B7A8D;letter-spacing:0.12em;
             text-transform:uppercase;margin-top:2px;">KPR Simulator 2026</div>
    </div>
    <hr style="border-color:rgba(201,168,76,0.2);margin:0.5rem 0 1rem">
    """, unsafe_allow_html=True)

    st.markdown("**📐 Tipe Rumah**")
    tipe_lantai = st.selectbox("Jumlah Lantai", ["1 Lantai", "2 Lantai", "3 Lantai"], index=1)

    st.markdown("---")
    st.markdown("**💰 Harga & Pembayaran**")

    harga_rumah = st.number_input(
        "Harga Rumah (Rp)",
        min_value=500_000_000,
        max_value=20_000_000_000,
        value=3_500_000_000,
        step=50_000_000,
        format="%d",
    )
    # Tampilkan angka dengan titik biar jelas berapa milyar
    st.markdown(
        f'<div class="harga-display">Rp {fmt_ribuan(harga_rumah)}</div>',
        unsafe_allow_html=True
    )

    dp_pct = st.slider("Down Payment (%)", min_value=0, max_value=90, value=20, step=1)

    utj = st.number_input(
        "UTJ – Uang Tanda Jadi (Rp)",
        min_value=0,
        max_value=500_000_000,
        value=15_000_000,
        step=1_000_000,
        format="%d",
    )
    st.markdown(
        f'<div class="harga-display" style="font-size:0.9rem;">Rp {fmt_ribuan(utj)}</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**📊 Kredit**")
    bunga = st.slider("Suku Bunga (%/tahun)", min_value=3.0, max_value=15.0, value=4.75, step=0.25, format="%.2f")
    tenor = st.slider("Tenor (tahun)", min_value=1, max_value=30, value=15, step=1)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#6B7A8D;line-height:1.7;padding:0.25rem 0">
        📋 <strong style="color:#C9A84C">Free PPN 2026:</strong><br>
        &lt; Rp 2 M → DTP 11% full<br>
        ≥ Rp 2 M → Flat Rp 220 Juta<br><br>
        ⚠️ <em>Simulasi estimasi. Angka final tergantung kebijakan bank &amp; notaris.</em>
    </div>
    """, unsafe_allow_html=True)


# ─── Kalkulasi ────────────────────────────────────────────────────────────────
dp_nominal    = harga_rumah * dp_pct / 100
sisa_dp_bayar = max(dp_nominal - utj, 0)
pokok_kpr     = harga_rumah - dp_nominal

ppn_dtp, ppn_rate_eff, ppn_ket, bawah_2m = hitung_ppn(harga_rumah)

# PPN ditanggung pemerintah → tidak masuk beban pembeli
# Pembeli tetap bayar: DP + AJB + BPHTB
ajb   = harga_rumah * 0.005
bphtb = harga_rumah * 0.05

total_biaya_transaksi = ajb + bphtb          # PPN tidak masuk beban pembeli
total_modal_awal      = dp_nominal + total_biaya_transaksi

tenor_bulan     = tenor * 12
angsuran_bln    = hitung_angsuran(pokok_kpr, bunga, tenor_bulan)
total_bayar_kpr = angsuran_bln * tenor_bulan
total_bunga     = total_bayar_kpr - pokok_kpr

tipe_icon = {"1 Lantai": "🏠", "2 Lantai": "🏡", "3 Lantai": "🏰"}[tipe_lantai]


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-wrap">
    <div class="logo-row">
        <div class="logo-icon">🏠</div>
        <div>
            <div class="brand-name">Ruang Masbay</div>
            <div class="brand-tagline">Property Intelligence · Est. 2024</div>
        </div>
    </div>
    <div class="gold-divider" style="margin:0.75rem 0"></div>
    <div class="header-title">Simulasi KPR – Free PPN 2026</div>
    <div class="header-sub">
        {tipe_icon} Rumah {tipe_lantai} &nbsp;·&nbsp;
        Suku Bunga {bunga:.2f}%/thn &nbsp;·&nbsp;
        Tenor {tenor} Tahun &nbsp;·&nbsp;
        📅 {datetime.now().strftime("%d %B %Y")}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Angsuran Hero ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="angsuran-box">
    <div class="angsuran-label">Estimasi Angsuran Bulanan</div>
    <div class="angsuran-value">{fmt_idr_short(angsuran_bln)}</div>
    <div class="angsuran-sub">
        Tenor {tenor} tahun ({tenor_bulan} bulan) &nbsp;·&nbsp;
        Bunga {bunga:.2f}%/thn &nbsp;·&nbsp;
        Pokok KPR {fmt_idr_short(pokok_kpr)}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Metric Cards ─────────────────────────────────────────────────────────────
if bawah_2m:
    ppn_color = "#2ECC71"
    ppn_disp  = "DTP 11% FULL"
    ppn_note  = f"Pemerintah tanggung Rp {fmt_ribuan(int(ppn_dtp))}"
else:
    ppn_color = "#E8C97B"
    ppn_disp  = "FREE Rp 220 Jt"
    ppn_note  = "Pemerintah tanggung Rp 220.000.000"

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Harga Rumah</div>
        <div class="metric-value big">{fmt_idr_short(harga_rumah)}</div>
        <div class="metric-note">{tipe_icon} {tipe_lantai} &nbsp;·&nbsp; Rp {fmt_ribuan(int(harga_rumah))}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Down Payment ({dp_pct}%)</div>
        <div class="metric-value">{fmt_idr_short(dp_nominal)}</div>
        <div class="metric-note">UTJ: Rp {fmt_ribuan(int(utj))} &nbsp;·&nbsp; Sisa: {fmt_idr_short(sisa_dp_bayar)}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Pokok KPR</div>
        <div class="metric-value">{fmt_idr_short(pokok_kpr)}</div>
        <div class="metric-note">Harga &minus; DP</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Free PPN 2026 🎁</div>
        <div class="metric-value" style="color:{ppn_color}">{ppn_disp}</div>
        <div class="metric-note">{ppn_note}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Total Bunga KPR</div>
        <div class="metric-value">{fmt_idr_short(total_bunga)}</div>
        <div class="metric-note">Selama {tenor} tahun</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Modal Awal Pembeli</div>
        <div class="metric-value">{fmt_idr_short(total_modal_awal)}</div>
        <div class="metric-note">DP + AJB + BPHTB (PPN ditanggung negara)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Info PPN ─────────────────────────────────────────────────────────────────
if bawah_2m:
    ppn_info = (
        f"✅ <strong>FREE PPN DTP 100%!</strong> "
        f"Harga rumah <strong>Rp {fmt_ribuan(int(harga_rumah))}</strong> berada di bawah Rp 2 Miliar. "
        f"PPN 11% sebesar <strong>Rp {fmt_ribuan(int(ppn_dtp))}</strong> "
        f"sepenuhnya <strong>Ditanggung Pemerintah</strong>. Pembeli tidak perlu bayar PPN sama sekali."
    )
else:
    ppn_info = (
        f"⚡ <strong>FREE PPN Rp 220.000.000!</strong> "
        f"Harga rumah <strong>Rp {fmt_ribuan(int(harga_rumah))}</strong> di atas Rp 2 Miliar. "
        f"Pemerintah menanggung PPN flat sebesar <strong>Rp 220.000.000</strong>. "
        f"Sisa PPN di luar Rp 220 Jt ({ppn_rate_eff:.2f}% dari harga) menjadi tanggungan pembeli."
    )

st.markdown(f'<div class="info-box">{ppn_info}</div>', unsafe_allow_html=True)

# ─── Dua Kolom ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-title">Rincian Harga & Biaya Transaksi</div>', unsafe_allow_html=True)

    if bawah_2m:
        ppn_tag      = '<span class="tag-free">DTP 11% FULL</span>'
        ppn_rate_str = "11.00%"
        ppn_nominal_str = f"Rp {fmt_ribuan(int(ppn_dtp))} (ditanggung pemerintah)"
    else:
        ppn_tag      = '<span class="tag-220">FREE Rp 220 Jt</span>'
        ppn_rate_str = f"{ppn_rate_eff:.2f}%"
        ppn_nominal_str = "Rp 220.000.000 (ditanggung pemerintah)"

    st.markdown(f"""
    <table class="calc-table">
        <thead>
            <tr><th>Komponen</th><th>Rate</th><th style="text-align:right">Nominal</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>Harga Rumah ({tipe_lantai})</td>
                <td>—</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(harga_rumah))}</td>
            </tr>
            <tr>
                <td>Free PPN 2026 &nbsp;{ppn_tag}</td>
                <td>{ppn_rate_str}</td>
                <td style="text-align:right;color:#2ECC71;font-size:0.8rem">{ppn_nominal_str}</td>
            </tr>
            <tr>
                <td>Biaya AJB (Akta Jual Beli)</td>
                <td>0.5%</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(ajb))}</td>
            </tr>
            <tr>
                <td>BPHTB (Bea Perolehan Hak)</td>
                <td>5%</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(bphtb))}</td>
            </tr>
            <tr class="highlight">
                <td colspan="2">Total Biaya Transaksi (beban pembeli)</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(total_biaya_transaksi))}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Rincian Down Payment</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="calc-table">
        <thead>
            <tr><th>Komponen</th><th style="text-align:right">Nominal</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>DP ({dp_pct}% &times; Rp {fmt_ribuan(int(harga_rumah))})</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(dp_nominal))}</td>
            </tr>
            <tr>
                <td>UTJ – Uang Tanda Jadi (sudah bayar)</td>
                <td style="text-align:right">&minus; Rp {fmt_ribuan(int(utj))}</td>
            </tr>
            <tr class="highlight">
                <td>Sisa DP yang Harus Dibayar</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(sisa_dp_bayar))}</td>
            </tr>
            <tr>
                <td>+ AJB + BPHTB</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(total_biaya_transaksi))}</td>
            </tr>
            <tr class="total-row">
                <td>💼 Total Modal Awal Pembeli</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(total_modal_awal))}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-title">Rincian Kredit (KPR)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="calc-table">
        <thead>
            <tr><th>Komponen</th><th style="text-align:right">Nilai</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>Pokok Pinjaman (KPR)</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(pokok_kpr))}</td>
            </tr>
            <tr>
                <td>Suku Bunga</td>
                <td style="text-align:right">{bunga:.2f}% / tahun</td>
            </tr>
            <tr>
                <td>Tenor</td>
                <td style="text-align:right">{tenor} tahun ({tenor_bulan} bulan)</td>
            </tr>
            <tr class="highlight">
                <td>📅 Angsuran / Bulan</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(angsuran_bln))}</td>
            </tr>
            <tr>
                <td>Total Pembayaran KPR</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(total_bayar_kpr))}</td>
            </tr>
            <tr>
                <td>Total Bunga</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(total_bunga))}</td>
            </tr>
            <tr class="total-row">
                <td>📊 Total Pengeluaran Pembeli</td>
                <td style="text-align:right">Rp {fmt_ribuan(int(total_modal_awal + total_bayar_kpr))}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Tabel Amortisasi (per Bulan)</div>', unsafe_allow_html=True)
    amort_rows = buat_amortisasi(pokok_kpr, bunga, tenor_bulan)
    df_amort = pd.DataFrame(amort_rows)
    for col in ["Angsuran", "Bunga", "Pokok", "Sisa Pokok"]:
        df_amort[col] = df_amort[col].apply(lambda x: "Rp " + fmt_ribuan(x))
    st.dataframe(df_amort, use_container_width=True, height=360)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box" style="font-size:0.78rem;color:#9BA8B5;line-height:1.7">
    📌 <strong style="color:#E8C97B">Catatan Penting:</strong>
    Simulasi menggunakan metode <strong style="color:#E8C97B">anuitas</strong> (angsuran tetap setiap bulan).
    Biaya AJB 0,5% dan BPHTB 5% adalah estimasi standar — dapat berbeda tergantung notaris/PPAT.
    <strong style="color:#E8C97B">Free PPN 2026:</strong>
    harga &lt; Rp 2 M = DTP 11% full &nbsp;|&nbsp;
    harga &ge; Rp 2 M = Free PPN flat <strong style="color:#E8C97B">Rp 220.000.000</strong> ditanggung pemerintah.
    Konsultasikan dengan agen properti atau banker Anda untuk angka final.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    &copy; {datetime.now().year} <span>Ruang Masbay</span> &nbsp;·&nbsp; All Rights Reserved<br>
    <span style="font-size:0.68rem">Simulasi KPR Free PPN 2026 &nbsp;·&nbsp; Powered by Ruang Masbay Property Intelligence</span>
</div>
""", unsafe_allow_html=True)
