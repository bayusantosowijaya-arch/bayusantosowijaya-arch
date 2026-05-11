import streamlit as st
import math
import locale
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Simulasi KPR – Ruang Masbay",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:    #C9A84C;
    --gold-lt: #E8C97B;
    --navy:    #0D1B2A;
    --navy-lt: #152336;
    --cream:   #F5F0E8;
    --slate:   #6B7A8D;
    --green:   #2ECC71;
    --red:     #E74C3C;
    --white:   #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--cream);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B2A 0%, #152336 100%);
    border-right: 1px solid rgba(201,168,76,0.3);
}
[data-testid="stSidebar"] .stSlider > div > div > div {
    background: var(--gold) !important;
}
[data-testid="stSidebar"] label {
    color: var(--cream) !important;
    font-weight: 500;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.header-wrap {
    background: linear-gradient(135deg, #152336 0%, #0D1B2A 60%, #1a2840 100%);
    border: 1px solid rgba(201,168,76,0.35);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.header-wrap::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(201,168,76,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.logo-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}
