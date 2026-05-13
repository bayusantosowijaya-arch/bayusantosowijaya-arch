import streamlit as st
import pandas as pd
from datetime import datetime

PASSWORD_AKSES = "KPR2026" 

st.set_page_config(
    page_title="Simulasi KPR Free PPN - Ruang Masbay",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
) 

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔐 KPR Simulator 2026 - Mas Bay")
    st.info("Untuk mendapatkan password akses, hubungi WhatsApp: 0878-8425-6765")
    
    user_input = st.text_input("Masukkan Password Akses:", type="password")
    
    if st.button("Buka Aplikasi"):
        if user_input == PASSWORD_AKSES:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Password salah! Silakan hubungi admin.")
    st.stop() 

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --gold: #D4AF37;
    --bg-black: #0A0F12;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-black);
    color: #F8F9FA;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #070B0D;
    border-right: 1px solid rgba(212, 175, 55, 0.2);
}

.brand-header {
    text-align: center;
    padding: 2.5rem 0;
    border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    margin-bottom: 2rem;
}

.brand-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.5rem;
    color: var(--gold);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.hero-box {
    background: linear-gradient(180deg, #12181E 0%, #0A0F12 100%);
    border: 1px solid rgba(212, 175, 55, 0.3);
    padding: 4rem;
    text-align: center;
    margin-bottom: 2.5rem;
}

.luxury-table {
    width: 100%;
    margin-top: 1rem;
}

.luxury-table td {
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.val-gold {
    text-align: right;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    color: var(--gold);
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def rb(v):
    return "{:,.0f}".format(int(v)).replace(",", ".")

def sh(v):
    if v >= 1_000_000_000:
        b = v / 1_000_000_000
        s = "{:.3f}".format(b) if b < 10 else "{:.2f}".format(b)
        return "Rp " + s.replace(".", ",") + " M"
    elif v >= 1_000_000:
        return "Rp {:.1f} Jt".format(v / 1_000_000)
    return "Rp {:,.0f}".format(v).replace(",", ".")

def angsuran(p, b, n):
    if p <= 0 or n <= 0: return 0.0
    if b == 0: return p / n
    r = b / 100 / 12
    return p * r * (1 + r)**n / ((1 + r)**n - 1)

def amortisasi(p, b, n):
    rows, sisa, r = [], p, b / 100 / 12
    ang = angsuran(p, b, n)
    for i in range(1, n + 1):
        bln = sisa * r
        pkk = ang - bln
        sisa -= pkk
        rows.append({"Bulan": i, "Angsuran": round(ang), "Bunga": round(bln),
                     "Pokok": round(pkk), "Sisa Pokok": round(max(sisa, 0))})
    return rows


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem">
        <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:900;
             background:linear-gradient(135deg,#E8C97B,#C9A84C);-webkit-background-clip:text;
             -webkit-text-fill-color:transparent;background-clip:text;">🏠 Ruang Masbay</div>
        <div style="font-size:0.68rem;color:#6B7A8D;letter-spacing:0.12em;text-transform:uppercase;margin-top:2px;">
             KPR Free PPN 2026</div>
    </div>
    <hr style="border-color:rgba(201,168,76,0.2);margin:0.5rem 0 1rem">
    """, unsafe_allow_html=True)

    # ── MODE: Include / Exclude PPN ──
    st.markdown("**💡 Mode Harga**")
    mode = st.radio(
        "Harga yang diinput adalah:",
        options=["Include PPN (Harga sudah termasuk PPN)",
                 "Exclude PPN (Harga belum termasuk PPN)"],
        index=0,
        label_visibility="collapsed",
    )
    is_include = mode.startswith("Include")

    if is_include:
        st.markdown("""
        <div class="mode-box-inc">
            ✅ <strong>Include PPN</strong><br>
            Harga yang Anda masukkan <strong>sudah termasuk PPN 11%</strong>.<br>
            Sistem akan menghitung harga dasar (sebelum PPN) secara otomatis.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="mode-box-exc">
            🔢 <strong>Exclude PPN</strong><br>
            Harga yang Anda masukkan <strong>belum termasuk PPN 11%</strong>.<br>
            PPN akan ditambahkan di atas harga tersebut.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📐 Tipe Rumah**")
    tipe_lantai = st.selectbox("Jumlah Lantai", ["1 Lantai", "2 Lantai", "3 Lantai"], index=1)

    st.markdown("---")
    st.markdown("**💰 Harga & Pembayaran**")

    label_harga = "Harga Rumah Include PPN (Rp)" if is_include else "Harga Rumah Exclude PPN (Rp)"
    harga_input = st.number_input(
        label_harga,
        min_value=100_000_000,
        max_value=50_000_000_000,
        value=3_500_000_000,
        step=50_000_000,
        format="%d",
    )
    st.markdown(f'<div class="harga-display">Rp {rb(harga_input)}</div>', unsafe_allow_html=True)

    dp_pct = st.slider("Down Payment (%)", 0, 90, 20, 1)

    utj = st.number_input(
        "UTJ – Uang Tanda Jadi (Rp)",
        min_value=0, max_value=500_000_000,
        value=15_000_000, step=1_000_000, format="%d",
    )
    st.markdown(f'<div class="harga-display" style="font-size:0.88rem;">Rp {rb(utj)}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📊 Kredit**")
    bunga = st.slider("Suku Bunga (%/tahun)", 3.0, 20.0, 7.5, 0.25, format="%.2f")
    tenor = st.slider("Tenor (tahun)", 1, 30, 20, 1)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.71rem;color:#6B7A8D;line-height:1.8;padding:0.25rem 0">
        📋 <strong style="color:#C9A84C">Free PPN 2026</strong><br>
        Harga dasar &lt; Rp 2 M → DTP 11% full<br>
        Harga dasar &ge; Rp 2 M → Free Rp 220 Juta<br><br>
        ⚠️ <em>Simulasi estimasi. Angka final tergantung kebijakan bank &amp; notaris.</em>
    </div>""", unsafe_allow_html=True)


# ── Konversi Harga ─────────────────────────────────────────────────────────────
#
# Include PPN → harga_input = harga_dasar × 1.11
#   → harga_dasar = harga_input / 1.11
#   → ppn_teoritikal = harga_input - harga_dasar
#
# Exclude PPN → harga_input = harga_dasar
#   → harga_jual (inc PPN) = harga_dasar × 1.11
#   → ppn_teoritikal = harga_dasar × 0.11

PPN_RATE = 0.11

if is_include:
    harga_inc = harga_input                         # harga include PPN (yang tertera)
    harga_exc = harga_input / (1 + PPN_RATE)        # harga dasar / exclude PPN
    ppn_teoritikal = harga_inc - harga_exc
else:
    harga_exc = harga_input                         # harga dasar / exclude PPN
    harga_inc = harga_input * (1 + PPN_RATE)        # harga include PPN
    ppn_teoritikal = harga_exc * PPN_RATE

# ── Free PPN Logic berdasarkan harga DASAR (exclude PPN) ─────────────────────
#
# Harga dasar < Rp 2 M  → DTP 11% FULL (seluruh PPN ditanggung pemerintah)
# Harga dasar >= Rp 2 M → Free PPN Rp 220 Juta ditanggung pemerintah
#                          sisa PPN di atas Rp 220 Jt = beban pembeli

BATAS_FREE = 2_000_000_000

if harga_exc < BATAS_FREE:
    ppn_ditanggung = ppn_teoritikal        # 100% ditanggung pemerintah
    ppn_beban      = 0.0
    ppn_label      = "DTP 11% FULL"
    bawah_2m       = True
else:
    ppn_ditanggung = 220_000_000.0
    ppn_beban      = max(ppn_teoritikal - 220_000_000, 0)
    ppn_label      = "FREE Rp 220 Jt"
    bawah_2m       = False

# ── Harga KPR = harga dasar (exclude PPN) + PPN beban pembeli ────────────────
# Developer menjual rumah; yang jadi basis KPR = nilai properti (harga exc)
# + PPN yang harus dibayar pembeli (jika ada)
harga_kpr_basis = harga_exc + ppn_beban

# ── Biaya lain (AJB & BPHTB dari harga dasar) ────────────────────────────────
ajb   = harga_exc * 0.005
bphtb = harga_exc * 0.05

# ── DP & Pokok KPR ───────────────────────────────────────────────────────────
dp_nominal    = harga_kpr_basis * dp_pct / 100
sisa_dp       = max(dp_nominal - utj, 0)
pokok_kpr     = harga_kpr_basis - dp_nominal

# ── Total Modal & KPR ────────────────────────────────────────────────────────
total_biaya_trx = ppn_beban + ajb + bphtb
total_modal     = dp_nominal + total_biaya_trx

tenor_bulan    = tenor * 12
ang_bln        = angsuran(pokok_kpr, bunga, tenor_bulan)
total_kpr      = ang_bln * tenor_bulan
total_bunga    = total_kpr - pokok_kpr

tipe_icon = {"1 Lantai": "🏠", "2 Lantai": "🏡", "3 Lantai": "🏰"}[tipe_lantai]


# ── Header ───────────────────────────────────────────────────────────────────
mode_label = "Include PPN" if is_include else "Exclude PPN"
st.markdown(f"""
<div class="header-wrap">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem">
        <div style="font-size:2.6rem;line-height:1">🏠</div>
        <div>
            <div class="brand-name">Ruang Masbay</div>
            <div class="brand-tagline">Property Intelligence · Est. 2024</div>
        </div>
    </div>
    <div class="gold-divider" style="margin:0.75rem 0"></div>
    <div class="header-title">Simulasi KPR – Free PPN 2026</div>
    <div class="header-sub">
        {tipe_icon} {tipe_lantai} &nbsp;·&nbsp;
        Mode Harga: <strong style="color:var(--gold-lt)">{mode_label}</strong> &nbsp;·&nbsp;
        Bunga {bunga:.2f}%/thn &nbsp;·&nbsp;
        Tenor {tenor} Tahun &nbsp;·&nbsp;
        📅 {datetime.now().strftime("%d %B %Y")}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Harga Summary Box ─────────────────────────────────────────────────────────
col_ha, col_hb = st.columns(2, gap="medium")
with col_ha:
    st.markdown(f"""
    <div style="background:rgba(46,204,113,0.08);border:1px solid rgba(46,204,113,0.3);
         border-radius:12px;padding:1rem 1.25rem;text-align:center;">
        <div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;
             color:#2ECC71;margin-bottom:0.3rem;">Harga Exclude PPN (Harga Dasar)</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:900;
             color:#2ECC71;">Rp {rb(int(harga_exc))}</div>
        <div style="font-size:0.72rem;color:#6B7A8D;margin-top:0.3rem;">Basis penentuan Free PPN 2026</div>
    </div>""", unsafe_allow_html=True)
with col_hb:
    st.markdown(f"""
    <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.3);
         border-radius:12px;padding:1rem 1.25rem;text-align:center;">
        <div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;
             color:var(--gold-lt);margin-bottom:0.3rem;">Harga Include PPN (Harga Jual)</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:900;
             color:var(--gold);">Rp {rb(int(harga_inc))}</div>
        <div style="font-size:0.72rem;color:#6B7A8D;margin-top:0.3rem;">PPN 11% = Rp {rb(int(ppn_teoritikal))}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)

# ── Angsuran Hero ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="angsuran-box">
    <div class="angsuran-label">Estimasi Angsuran Bulanan</div>
    <div class="angsuran-value">{sh(ang_bln)}</div>
    <div class="angsuran-sub">
        Tenor {tenor} tahun ({tenor_bulan} bulan) &nbsp;·&nbsp;
        Bunga {bunga:.2f}%/thn &nbsp;·&nbsp;
        Pokok KPR {sh(pokok_kpr)}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric Cards ──────────────────────────────────────────────────────────────
ppn_card_color = "#2ECC71" if bawah_2m else "#E8C97B"
ppn_card_val   = "DTP 11% FULL" if bawah_2m else "FREE Rp 220 Jt"
ppn_card_note  = f"Pemerintah tanggung Rp {rb(int(ppn_ditanggung))}" if bawah_2m else f"Beban pembeli Rp {rb(int(ppn_beban))}"

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Harga Exclude PPN</div>
        <div class="metric-value big">{sh(harga_exc)}</div>
        <div class="metric-note">Harga dasar sebelum PPN</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Harga Include PPN</div>
        <div class="metric-value">{sh(harga_inc)}</div>
        <div class="metric-note">Harga jual ke pembeli</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Free PPN 2026 🎁</div>
        <div class="metric-value" style="color:{ppn_card_color}">{ppn_card_val}</div>
        <div class="metric-note">{ppn_card_note}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Down Payment ({dp_pct}%)</div>
        <div class="metric-value">{sh(dp_nominal)}</div>
        <div class="metric-note">UTJ: Rp {rb(int(utj))} &nbsp;·&nbsp; Sisa: {sh(sisa_dp)}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Pokok KPR</div>
        <div class="metric-value">{sh(pokok_kpr)}</div>
        <div class="metric-note">Harga KPR &minus; DP</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Modal Awal Pembeli</div>
        <div class="metric-value">{sh(total_modal)}</div>
        <div class="metric-note">DP + Biaya Transaksi</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Info PPN ──────────────────────────────────────────────────────────────────
if bawah_2m:
    info = (f"✅ <strong>FREE PPN DTP 100%!</strong> "
            f"Harga dasar (exclude PPN) <strong>Rp {rb(int(harga_exc))}</strong> "
            f"berada di bawah Rp 2 Miliar. PPN 11% = <strong>Rp {rb(int(ppn_teoritikal))}</strong> "
            f"sepenuhnya <strong>Ditanggung Pemerintah</strong>. Pembeli tidak perlu bayar PPN.")
else:
    info = (f"⚡ <strong>FREE PPN Rp 220.000.000!</strong> "
            f"Harga dasar (exclude PPN) <strong>Rp {rb(int(harga_exc))}</strong> "
            f"di atas Rp 2 Miliar. PPN total = <strong>Rp {rb(int(ppn_teoritikal))}</strong>. "
            f"Pemerintah tanggung <strong>Rp 220.000.000</strong>. "
            f"Sisa beban pembeli = <strong>Rp {rb(int(ppn_beban))}</strong>.")

st.markdown(f'<div class="info-box">{info}</div>', unsafe_allow_html=True)

# ── Dua Kolom: Rincian ────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Tabel Konversi Harga
    st.markdown('<div class="section-title">Konversi Harga PPN</div>', unsafe_allow_html=True)
    ppn_tag = f'<span class="tag-free">DTP 11% FULL</span>' if bawah_2m else f'<span class="tag-220">FREE Rp 220 Jt</span>'
    st.markdown(f"""
    <table class="calc-table">
        <thead><tr><th>Komponen</th><th style="text-align:right">Nominal</th></tr></thead>
        <tbody>
            <tr>
                <td>Harga Exclude PPN (Harga Dasar)</td>
                <td style="text-align:right;color:#2ECC71">Rp {rb(int(harga_exc))}</td>
            </tr>
            <tr>
                <td>PPN 11% (Teoritikal)</td>
                <td style="text-align:right">Rp {rb(int(ppn_teoritikal))}</td>
            </tr>
            <tr>
                <td>Harga Include PPN (Harga Jual)</td>
                <td style="text-align:right;color:var(--gold-lt)">Rp {rb(int(harga_inc))}</td>
            </tr>
            <tr style="background:rgba(46,204,113,0.06)">
                <td>Free PPN ditanggung pemerintah &nbsp;{ppn_tag}</td>
                <td style="text-align:right;color:#2ECC71">&minus; Rp {rb(int(ppn_ditanggung))}</td>
            </tr>
            <tr class="hl">
                <td>PPN Beban Pembeli</td>
                <td style="text-align:right;color:{'#2ECC71' if ppn_beban==0 else '#E74C3C'}">
                    {'NIHIL / Rp 0' if ppn_beban == 0 else 'Rp ' + rb(int(ppn_beban))}
                </td>
            </tr>
        </tbody>
    </table>""", unsafe_allow_html=True)

    # Tabel Biaya Transaksi
    st.markdown('<div class="section-title">Biaya Transaksi</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="calc-table">
        <thead><tr><th>Komponen</th><th>Rate</th><th style="text-align:right">Nominal</th></tr></thead>
        <tbody>
            <tr>
                <td>PPN Beban Pembeli</td>
                <td>—</td>
                <td style="text-align:right;color:{'#2ECC71' if ppn_beban==0 else '#E74C3C'}">
                    {'NIHIL' if ppn_beban == 0 else 'Rp ' + rb(int(ppn_beban))}
                </td>
            </tr>
            <tr>
                <td>Biaya AJB (dari harga dasar)</td>
                <td>0.5%</td>
                <td style="text-align:right">Rp {rb(int(ajb))}</td>
            </tr>
            <tr>
                <td>BPHTB (dari harga dasar)</td>
                <td>5%</td>
                <td style="text-align:right">Rp {rb(int(bphtb))}</td>
            </tr>
            <tr class="hl">
                <td colspan="2">Total Biaya Transaksi</td>
                <td style="text-align:right">Rp {rb(int(total_biaya_trx))}</td>
            </tr>
        </tbody>
    </table>""", unsafe_allow_html=True)

    # Tabel DP
    st.markdown('<div class="section-title">Rincian Down Payment</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="calc-table">
        <thead><tr><th>Komponen</th><th style="text-align:right">Nominal</th></tr></thead>
        <tbody>
            <tr>
                <td>Basis Harga KPR</td>
                <td style="text-align:right">Rp {rb(int(harga_kpr_basis))}</td>
            </tr>
            <tr>
                <td>DP ({dp_pct}%)</td>
                <td style="text-align:right">Rp {rb(int(dp_nominal))}</td>
            </tr>
            <tr>
                <td>UTJ – Uang Tanda Jadi</td>
                <td style="text-align:right">&minus; Rp {rb(int(utj))}</td>
            </tr>
            <tr class="hl">
                <td>Sisa DP yang Harus Dibayar</td>
                <td style="text-align:right">Rp {rb(int(sisa_dp))}</td>
            </tr>
            <tr>
                <td>+ Total Biaya Transaksi</td>
                <td style="text-align:right">Rp {rb(int(total_biaya_trx))}</td>
            </tr>
            <tr class="tot">
                <td>💼 Total Modal Awal Pembeli</td>
                <td style="text-align:right">Rp {rb(int(total_modal))}</td>
            </tr>
        </tbody>
    </table>""", unsafe_allow_html=True)

with col_right:
    # Tabel KPR
    st.markdown('<div class="section-title">Rincian Kredit (KPR)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="calc-table">
        <thead><tr><th>Komponen</th><th style="text-align:right">Nilai</th></tr></thead>
        <tbody>
            <tr>
                <td>Basis Harga KPR</td>
                <td style="text-align:right">Rp {rb(int(harga_kpr_basis))}</td>
            </tr>
            <tr>
                <td>Down Payment ({dp_pct}%)</td>
                <td style="text-align:right">Rp {rb(int(dp_nominal))}</td>
            </tr>
            <tr>
                <td>Pokok Pinjaman (KPR)</td>
                <td style="text-align:right">Rp {rb(int(pokok_kpr))}</td>
            </tr>
            <tr>
                <td>Suku Bunga</td>
                <td style="text-align:right">{bunga:.2f}% / tahun</td>
            </tr>
            <tr>
                <td>Tenor</td>
                <td style="text-align:right">{tenor} tahun ({tenor_bulan} bulan)</td>
            </tr>
            <tr class="hl">
                <td>📅 Angsuran / Bulan</td>
                <td style="text-align:right">Rp {rb(int(ang_bln))}</td>
            </tr>
            <tr>
                <td>Total Pembayaran KPR</td>
                <td style="text-align:right">Rp {rb(int(total_kpr))}</td>
            </tr>
            <tr>
                <td>Total Bunga</td>
                <td style="text-align:right">Rp {rb(int(total_bunga))}</td>
            </tr>
            <tr class="tot">
                <td>📊 Total Pengeluaran Pembeli</td>
                <td style="text-align:right">Rp {rb(int(total_modal + total_kpr))}</td>
            </tr>
        </tbody>
    </table>""", unsafe_allow_html=True)

    # Amortisasi
    st.markdown('<div class="section-title">Tabel Amortisasi (per Bulan)</div>', unsafe_allow_html=True)
    df = pd.DataFrame(amortisasi(pokok_kpr, bunga, tenor_bulan))
    for c in ["Angsuran", "Bunga", "Pokok", "Sisa Pokok"]:
        df[c] = df[c].apply(lambda x: "Rp " + rb(x))
    st.dataframe(df, use_container_width=True, height=370)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="info-box" style="font-size:0.78rem;color:#9BA8B5;line-height:1.8">
    📌 <strong style="color:#E8C97B">Catatan Penting:</strong>
    Simulasi menggunakan metode <strong style="color:#E8C97B">anuitas</strong> (angsuran tetap).
    AJB 0,5% dan BPHTB 5% dihitung dari <strong style="color:#E8C97B">harga dasar (exclude PPN)</strong>.
    Free PPN 2026 ditentukan dari harga dasar:
    &lt; Rp 2 M = DTP 11% full &nbsp;|&nbsp;
    &ge; Rp 2 M = Free flat <strong style="color:#E8C97B">Rp 220.000.000</strong>.
    Konsultasikan dengan agen properti atau banker untuk angka final.
</div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    &copy; {datetime.now().year} <span>Ruang Masbay</span> &nbsp;&middot;&nbsp; All Rights Reserved<br>
    <span style="font-size:0.68rem">Simulasi KPR Free PPN 2026 &nbsp;&middot;&nbsp; Powered by Ruang Masbay Property Intelligence</span>
</div>""", unsafe_allow_html=True)
